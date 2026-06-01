# Backend Admin - Gestion Dataset

Backend sécurisé avec interface d'administration Vue.js pour la mise à jour de datasets via drag & drop et scraping web.

## 🚀 Fonctionnalités

- **Authentification sécurisée** avec mot de passe admin hashé
- **Upload par drag & drop** de fichiers JSON, CSV, TXT, XML
- **Scraping web automatique** avec détection de catégories
- **Interface Vue.js moderne** avec Bootstrap 5
- **API REST sécurisée** avec sessions
- **Gestion des datasets** en temps réel

## 📋 Prérequis

- Node.js (version 14 ou supérieure)
- npm ou yarn

## 🛠️ Installation

1. **Installer les dépendances :**
```bash
cd backend
npm install
```

2. **Démarrer le serveur :**
```bash
npm start
# ou pour le développement:
npm run dev
```

3. **Accéder à l'interface :**
- Ouvrir: `http://localhost:3000/admin`
- Mot de passe par défaut: `admin123`

## 🔒 Sécurité

### Authentification
- Mot de passe hashé avec bcrypt
- Sessions sécurisées avec express-session
- Protection des routes API avec middleware d'authentification

### Upload de fichiers
- Validation des types de fichiers (JSON, CSV, TXT, XML uniquement)
- Limitation de taille (10MB max)
- Stockage sécurisé dans dossier `uploads/`

### Protection contre les attaques
- CORS configuré
- Validation des entrées
- Timeout sur les requêtes de scraping
- User-Agent approprié pour le scraping

## 📁 Structure des fichiers

```
backend/
├── server.js          # Serveur Express principal
├── admin.html         # Interface Vue.js d'administration
├── package.json       # Dépendances et scripts
├── uploads/           # Dossier des fichiers uploadés (créé automatiquement)
└── ../data/           # Dossier du dataset (créé automatiquement)
    └── dataset.json   # Dataset principal
```

## 🌐 API Endpoints

### Authentification
- `POST /api/login` - Connexion admin
- `POST /api/logout` - Déconnexion
- `GET /api/auth-status` - Vérifier l'authentification

### Upload & Dataset
- `POST /api/upload` - Upload de fichiers (authentifié)
- `GET /api/dataset` - Récupérer le dataset (authentifié)
- `GET /api/categories` - Lister les catégories (authentifié)

### Scraping
- `POST /api/scrape` - Scraper une URL (authentifié)

## 📊 Format du Dataset

Le dataset est stocké en JSON avec la structure suivante :

```json
{
  "url_ou_cle": {
    "title": "Titre de la page",
    "url": "https://example.com",
    "scraped_at": "2024-01-01T12:00:00.000Z",
    "categories": ["governance", "technology"],
    "content": {
      "headings": [...],
      "links": [...],
      "paragraphs": [...]
    }
  }
}
```

## 🏷️ Détection automatique des catégories

Le système détecte automatiquement les catégories basées sur des mots-clés :

- **governance** : gouvernance, conseil, administration, mandataire
- **technology** : technologie, numérique, digital, informatique  
- **finance** : finance, économie, budget, investissement
- **legal** : juridique, loi, règlement, legal
- **management** : management, gestion, direction, leadership

## 🔧 Configuration

### Changer le mot de passe admin

1. Générer un nouveau hash :
```bash
node -e "console.log(require('bcrypt').hashSync('nouveau_mot_de_passe', 10))"
```

2. Remplacer `ADMIN_PASSWORD_HASH` dans `server.js`

### Variables d'environnement (optionnel)

```bash
PORT=3000
SESSION_SECRET=votre-secret-de-session-tres-long
```

## 🎨 Interface utilisateur

L'interface Vue.js offre :

- **Login sécurisé** avec design moderne
- **Zone de drag & drop** intuitive pour les fichiers
- **Formulaire de scraping** avec sélecteur CSS optionnel
- **Aperçu du dataset** en temps réel
- **Notifications** pour toutes les actions
- **Design responsive** avec Bootstrap 5

## 🚨 Sécurité recommandée en production

1. **Changer le mot de passe** par défaut
2. **Utiliser HTTPS** uniquement
3. **Configurer un firewall** pour limiter l'accès
4. **Ajouter un rate limiting** sur les endpoints d'authentification
5. **Configurer des logs** d'audit
6. **Utiliser des variables d'environnement** pour les secrets

## 🐛 Dépannage

### Erreur de permissions
```bash
sudo chown -R $USER:$USER uploads/
sudo chown -R $USER:$USER ../data/
```

### Port déjà utilisé
Changer le port dans le fichier ou variable d'environnement :
```bash
PORT=3001 npm start
```

### Problèmes de CORS
Vérifier la configuration CORS dans `server.js` si vous accédez depuis un autre domaine.

## 📝 License

MIT License - Libre d'utilisation pour vos projets.