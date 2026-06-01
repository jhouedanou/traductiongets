const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const cheerio = require('cheerio');
const axios = require('axios');
const bcrypt = require('bcrypt');
const session = require('express-session');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Configuration de session
app.use(session({
    secret: process.env.SESSION_SECRET || 'admin-secret-key-changeme',
    resave: false,
    saveUninitialized: false,
    cookie: { secure: false, maxAge: 24 * 60 * 60 * 1000 } // 24h
}));

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, '../')));

// Configuration multer pour upload
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const uploadDir = path.join(__dirname, '../uploads');
        if (!fs.existsSync(uploadDir)) {
            fs.mkdirSync(uploadDir, { recursive: true });
        }
        cb(null, uploadDir);
    },
    filename: (req, file, cb) => {
        const timestamp = Date.now();
        const ext = path.extname(file.originalname);
        cb(null, `${timestamp}-${file.originalname}`);
    }
});

const upload = multer({ 
    storage: storage,
    fileFilter: (req, file, cb) => {
        // Accepter seulement certains types de fichiers
        const allowedTypes = ['.json', '.csv', '.txt', '.xml'];
        const ext = path.extname(file.originalname).toLowerCase();
        if (allowedTypes.includes(ext)) {
            cb(null, true);
        } else {
            cb(new Error('Type de fichier non autorisé'), false);
        }
    },
    limits: { fileSize: 10 * 1024 * 1024 } // 10MB max
});

// Mot de passe admin (hashé)
const ADMIN_PASSWORD_HASH = '$2b$10$Yl8qTQBzBP4QxN9gJzUwSeGvXvYB8P1nKzQn8eGhWbcQvYbE8Z7W2'; // admin123

// Middleware d'authentification
const requireAuth = (req, res, next) => {
    if (req.session.isAuthenticated) {
        next();
    } else {
        res.status(401).json({ error: 'Non autorisé' });
    }
};

// Route de login
app.post('/api/login', async (req, res) => {
    try {
        const { password } = req.body;
        
        if (!password) {
            return res.status(400).json({ error: 'Mot de passe requis' });
        }

        const isValid = await bcrypt.compare(password, ADMIN_PASSWORD_HASH);
        
        if (isValid) {
            req.session.isAuthenticated = true;
            res.json({ success: true, message: 'Connecté avec succès' });
        } else {
            res.status(401).json({ error: 'Mot de passe incorrect' });
        }
    } catch (error) {
        res.status(500).json({ error: 'Erreur serveur' });
    }
});

// Route de logout
app.post('/api/logout', (req, res) => {
    req.session.destroy();
    res.json({ success: true, message: 'Déconnecté' });
});

// Vérifier le statut d'authentification
app.get('/api/auth-status', (req, res) => {
    res.json({ authenticated: !!req.session.isAuthenticated });
});

// Upload de fichiers
app.post('/api/upload', requireAuth, upload.single('file'), (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'Aucun fichier uploadé' });
        }

        const fileInfo = {
            originalName: req.file.originalname,
            filename: req.file.filename,
            size: req.file.size,
            uploadDate: new Date().toISOString(),
            path: req.file.path
        };

        // Traiter le fichier selon son type
        if (req.file.originalname.endsWith('.json')) {
            try {
                const content = fs.readFileSync(req.file.path, 'utf8');
                const data = JSON.parse(content);
                
                // Mettre à jour le dataset existant
                updateDataset(data);
                
                res.json({ 
                    success: true, 
                    message: 'Dataset mis à jour avec succès',
                    fileInfo: fileInfo,
                    recordsProcessed: Array.isArray(data) ? data.length : Object.keys(data).length
                });
            } catch (parseError) {
                res.status(400).json({ error: 'Erreur de parsing JSON' });
            }
        } else {
            res.json({ 
                success: true, 
                message: 'Fichier uploadé avec succès',
                fileInfo: fileInfo
            });
        }
    } catch (error) {
        res.status(500).json({ error: 'Erreur lors de l\'upload' });
    }
});

// Fonction pour mettre à jour le dataset
function updateDataset(newData) {
    const dataFile = path.join(__dirname, '../data/dataset.json');
    
    // Créer le dossier data s'il n'existe pas
    const dataDir = path.dirname(dataFile);
    if (!fs.existsSync(dataDir)) {
        fs.mkdirSync(dataDir, { recursive: true });
    }

    let existingData = {};
    
    // Charger les données existantes
    if (fs.existsSync(dataFile)) {
        try {
            const content = fs.readFileSync(dataFile, 'utf8');
            existingData = JSON.parse(content);
        } catch (error) {
            console.log('Erreur lecture dataset existant:', error);
        }
    }

    // Fusionner avec les nouvelles données
    const mergedData = { ...existingData, ...newData };
    
    // Sauvegarder
    fs.writeFileSync(dataFile, JSON.stringify(mergedData, null, 2));
    
    return mergedData;
}

// Scraper de pages web
app.post('/api/scrape', requireAuth, async (req, res) => {
    try {
        const { url, selector } = req.body;
        
        if (!url) {
            return res.status(400).json({ error: 'URL requise' });
        }

        const response = await axios.get(url, {
            timeout: 10000,
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        });

        const $ = cheerio.load(response.data);
        
        const scrapedData = {
            url: url,
            title: $('title').text().trim(),
            scraped_at: new Date().toISOString(),
            content: {}
        };

        if (selector) {
            // Utiliser le sélecteur spécifique
            scrapedData.content.selected = $(selector).map((i, el) => $(el).text().trim()).get();
        } else {
            // Scraper automatique des éléments communs
            scrapedData.content.headings = $('h1, h2, h3').map((i, el) => ({
                tag: el.tagName,
                text: $(el).text().trim()
            })).get();
            
            scrapedData.content.links = $('a[href]').map((i, el) => ({
                text: $(el).text().trim(),
                href: $(el).attr('href')
            })).get().slice(0, 20); // Limiter à 20 liens
            
            scrapedData.content.paragraphs = $('p').map((i, el) => $(el).text().trim()).get().slice(0, 10);
        }

        // Détecter les catégories basées sur le contenu
        const categories = detectCategories(scrapedData);
        scrapedData.categories = categories;

        // Sauvegarder dans le dataset
        updateDataset({ [url]: scrapedData });

        res.json({ 
            success: true, 
            message: 'Page scrapée avec succès',
            data: scrapedData
        });

    } catch (error) {
        console.error('Erreur scraping:', error);
        res.status(500).json({ error: 'Erreur lors du scraping: ' + error.message });
    }
});

// Fonction de détection de catégories
function detectCategories(data) {
    const categories = [];
    const content = JSON.stringify(data.content).toLowerCase();
    
    // Mots-clés pour détecter les catégories
    const keywords = {
        'governance': ['gouvernance', 'conseil', 'administration', 'mandataire'],
        'technology': ['technologie', 'numérique', 'digital', 'informatique'],
        'finance': ['finance', 'économie', 'budget', 'investissement'],
        'legal': ['juridique', 'loi', 'règlement', 'legal'],
        'management': ['management', 'gestion', 'direction', 'leadership']
    };

    for (const [category, words] of Object.entries(keywords)) {
        if (words.some(word => content.includes(word))) {
            categories.push(category);
        }
    }

    return categories.length > 0 ? categories : ['general'];
}

// API pour récupérer le dataset
app.get('/api/dataset', requireAuth, (req, res) => {
    try {
        const dataFile = path.join(__dirname, '../data/dataset.json');
        
        if (fs.existsSync(dataFile)) {
            const content = fs.readFileSync(dataFile, 'utf8');
            const data = JSON.parse(content);
            res.json(data);
        } else {
            res.json({});
        }
    } catch (error) {
        res.status(500).json({ error: 'Erreur lecture dataset' });
    }
});

// API pour obtenir les catégories
app.get('/api/categories', requireAuth, (req, res) => {
    try {
        const dataFile = path.join(__dirname, '../data/dataset.json');
        
        if (fs.existsSync(dataFile)) {
            const content = fs.readFileSync(dataFile, 'utf8');
            const data = JSON.parse(content);
            
            const categories = new Set();
            Object.values(data).forEach(item => {
                if (item.categories) {
                    item.categories.forEach(cat => categories.add(cat));
                }
            });
            
            res.json(Array.from(categories));
        } else {
            res.json([]);
        }
    } catch (error) {
        res.status(500).json({ error: 'Erreur lecture catégories' });
    }
});

// Route pour l'interface admin
app.get('/admin', (req, res) => {
    res.sendFile(path.join(__dirname, 'admin.html'));
});

// Démarrage du serveur
app.listen(PORT, () => {
    console.log(`Serveur démarré sur le port ${PORT}`);
    console.log(`Interface admin disponible sur: http://localhost:${PORT}/admin`);
    console.log(`Mot de passe admin par défaut: admin123`);
});

module.exports = app;