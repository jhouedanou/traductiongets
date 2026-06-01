# Guide d'utilisation du Template d'Article

Ce document explique comment utiliser le template d'article (`article-template.html`) pour créer de nouveaux articles avec une mise en forme cohérente et élégante.

## Fichiers du Template

- `article-template.html` : Template principal à copier pour créer un nouvel article
- `README-TEMPLATE.md` : Ce guide d'utilisation

## Étapes pour créer un nouvel article

### 1. Copier le template
```bash
cp pages/article-template.html pages/mon-nouvel-article.html
```

### 2. Remplacer les placeholders

Remplacez les éléments suivants dans le fichier copié :

#### Métadonnées principales
- `[TITRE_ARTICLE]` : Le titre de votre article
- `[CATEGORIE]` : La catégorie principale (ex: "Généralités", "Féminisation", etc.)
- `[SOUS_CATEGORIE]` : La sous-catégorie (ex: "Contributions", "Documents utiles")
- `[DATE_PUBLICATION]` : Date de publication (format : "24 septembre 2025")

#### Contenu de l'article
- `[PARAGRAPHE_INTRODUCTION]` : Paragraphe d'introduction mis en valeur
- `[CONTENU_ARTICLE]` : Le contenu principal de l'article

#### Image (optionnel)
Si votre article a une image :
1. Décommentez la section "Article image"
2. Remplacez :
   - `[CHEMIN_IMAGE]` : Chemin vers l'image (ex: `../images/mon-image.jpg`)
   - `[ALT_IMAGE]` : Texte alternatif pour l'image

#### Informations auteur (optionnel)
Si vous voulez ajouter des informations sur l'auteur :
1. Décommentez la section "author-info"
2. Remplacez `[INFO_AUTEUR]` par les informations de l'auteur

### 3. Structurer le contenu

Le template offre plusieurs classes CSS pour structurer votre contenu :

#### Paragraphe normal
```html
<p>Votre texte ici...</p>
```

#### Sous-titre
```html
<h3 class="article-subtitle">Votre sous-titre</h3>
```

#### Citation mise en valeur
```html
<p><span class="quote-highlight">Citation importante</span></p>
```

#### Liste dans un encadré
```html
<div class="article-list">
    <ul>
        <li>Premier élément</li>
        <li>Deuxième élément</li>
    </ul>
</div>
```

#### Encadré de mise en valeur
```html
<div class="highlight-box">
    <p>Contenu important à mettre en valeur</p>
</div>
```

### 4. Ajouter l'article à la homepage

Une fois votre article créé, ajoutez-le au dataset dans `index.html` :

1. Trouvez la section `dataSets` dans le script JavaScript
2. Ajoutez votre article dans la catégorie appropriée :

```javascript
'generalites-contrib': [
    { title: 'Mon Nouvel Article', url: 'pages/mon-nouvel-article.html' },
    // ... autres articles
],
```

## Exemple complet

Voici un exemple de remplacement des placeholders :

```html
<!-- Avant -->
<title>[TITRE_ARTICLE] - G-ET-S</title>
<h1 class="display-8">[TITRE_ARTICLE]</h1>

<!-- Après -->
<title>L'Évolution de la Gouvernance - G-ET-S</title>
<h1 class="display-8">L'Évolution de la Gouvernance</h1>
```

## Caractéristiques du Design

Le template offre :

- **Design moderne** : Couleurs cohérentes avec le site, ombres et bordures arrondies
- **Responsive** : S'adapte automatiquement aux écrans mobiles
- **Animations** : Effets de survol et animation d'entrée
- **Typographie élégante** : Hiérarchie claire des titres et textes
- **Images optimisées** : Redimensionnement automatique avec effet de survol
- **Navigation intuitive** : Breadcrumb et bouton de retour à l'accueil

## Conseils d'utilisation

1. **Gardez la cohérence** : Utilisez toujours le même format pour les dates et catégories
2. **Optimisez les images** : Utilisez des images de bonne qualité mais pas trop lourdes
3. **Structurez le contenu** : Utilisez les sous-titres et encadrés pour faciliter la lecture
4. **Testez la responsive** : Vérifiez l'affichage sur mobile et tablette
5. **Mettez à jour la homepage** : N'oubliez pas d'ajouter votre article au dataset

## Maintenance

Pour maintenir la cohérence :

1. **Styles globaux** : Les modifications de style doivent être faites dans le template principal
2. **Versions** : Documentez les changements majeurs du template
3. **Tests** : Testez les nouveaux articles sur différents navigateurs

Ce template garantit une présentation professionnelle et cohérente pour tous les articles du site G-ET-S.