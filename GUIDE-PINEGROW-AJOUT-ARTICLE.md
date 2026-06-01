# Guide Pinegrow : Créer et publier un nouvel article

Ce guide explique comment créer un nouvel article sur le site G-ET-S en utilisant Pinegrow. Le système de génération automatique du JSON détectera automatiquement votre nouvel article.

---

### Comment ça fonctionne ?

1. Le script surveille le DOM de la page `index.html`
2. Il détecte automatiquement tous les liens (`item-link`) présents dans les colonnes
3. Il génère le dataset à partir des titres et URLs trouvés
4. Il met à jour le dataset en temps réel lors de modifications

**Vous n'avez donc PAS besoin de modifier manuellement le JSON dans `index.html` !**

---

## Étape 1 : Créer le modèle de page (01.html)

### 1.1 Dupliquer le template

1. Ouvrez Pinegrow
2. Dans le panneau **Files** (volet gauche), naviguez vers le dossier `pages/`
3. Faites un **clic droit** sur le fichier `0-template.html`
4. Sélectionnez **Duplicate file** (ou copiez-collez le fichier)
5. Renommez le fichier en `01.html`

### 1.2 Structure du modèle

Le fichier `0-template.html` contient déjà :
- Les balises `<head>` avec tous les liens CSS nécessaires
- Le header et la navigation (chargés via includes)
- Le breadcrumb de navigation
- La structure d'article avec :
  - Titre principal (`<h1>`)
  - Date de publication
  - Catégorie
  - Zone de contenu
  - Boutons de navigation
- Le footer

---

## Étape 2 : Créer votre article

### 2.1 Dupliquer le modèle pour votre article

1. Dans Pinegrow, dans le dossier `pages/`
2. Faites un **clic droit** sur `01.html`
3. Sélectionnez **Duplicate file**
4. Renommez le fichier selon votre article, par exemple : `mon-nouvel-article.html`

### 2.2 Modifier le contenu dans Pinegrow

#### Modifier le titre et les métadonnées

1. **Double-cliquez** sur le `<title>` dans la vue arbre ou le panneau Properties
2. Changez le titre en : `Mon Nouvel Article - G-ET-S`

3. **Sélectionnez** le `<h1>` (titre principal)
4. Modifiez le texte : `Mon Nouvel Article`

5. **Sélectionnez** la date de publication
6. Changez la date : `Publié le XX mois 2025`

7. **Sélectionnez** la catégorie (balise `<span>` après l'icône tag)
8. Modifiez selon la catégorie :
   - `Généralités - Contributions`
   - `Généralités - Documents utiles`
   - `Féminisation - Contributions`
   - `Féminisation - Documents utiles`
   - etc.

#### Modifier le breadcrumb

1. Localisez le `<nav aria-label="breadcrumb">`
2. Sélectionnez le dernier élément du breadcrumb
3. Changez le texte pour correspondre à votre article

#### Modifier le contenu

1. Localisez la `<div class="article-content">`
2. Supprimez le contenu existant dans `.card-body`
3. Ajoutez votre contenu :
   - Utilisez `<p class="lead">` pour le paragraphe d'introduction
   - Utilisez `<p>` pour les paragraphes normaux
   - Utilisez `<h2>`, `<h3>` pour les sous-titres
   - Utilisez `<ul>` et `<ol>` pour les listes
   - Utilisez `<blockquote class="blockquote">` pour les citations

**Astuce Pinegrow :** Vous pouvez ajouter des éléments depuis la **Library** (panneau gauche) en les glissant-déposant dans la zone de contenu.

#### Modifier les boutons de navigation (optionnel)

1. Localisez la section `<!-- Navigation buttons -->`
2. Modifiez les liens `href` si nécessaire
3. Changez les textes des boutons

### 2.3 Sauvegarder

1. **Ctrl+S** (Windows) ou **Cmd+S** (Mac)
2. Votre page est maintenant créée !

---

## Étape 3 : Ajouter le lien vers l'article dans l'index

### 3.1 Ouvrir index.html dans Pinegrow

1. Ouvrez `index.html` dans Pinegrow
2. Localisez la section avec le plateau d'accueil (7 colonnes)

### 3.2 Identifier la colonne cible

Les colonnes sont identifiées par leurs IDs :
- `list-generalites-contrib` → Généralités - Contributions de Guy Le Péchon
- `list-generalites-docs` → Généralités - Documents utiles
- `list-feminisation-contrib` → Féminisation - Contributions de Guy Le Péchon
- `list-feminisation-docs` → Féminisation - Documents utiles
- `list-qui` → Qui est G & S
- `list-pour-mandataires` → Pour mandataires
- `list-pour-societes` → Pour Sociétés

### 3.3 Ajouter votre article

#### Méthode visuelle dans Pinegrow

1. Dans la vue **Tree** (arbre DOM), localisez l'ID de la liste cible, par exemple `#list-generalites-contrib`

2. **Clic droit** sur le `<ul>` → **Add element**

3. Ajoutez un `<li>` avec la classe `list-item generalites-contrib` (adaptez selon votre catégorie)

4. À l'intérieur du `<li>`, ajoutez un `<a>` avec :
   - **Classe** : `item-link`
   - **Attribut href** : `pages/mon-nouvel-article.html`

5. À l'intérieur du `<a>`, ajoutez un `<span>` contenant le titre de votre article

#### Code HTML à insérer (référence)

Voici le code que vous devez créer (adapté à votre article) :

```html
<li class="list-item generalites-contrib">
    <a class="item-link" href="pages/mon-nouvel-article.html">
        <span>Mon Nouvel Article</span>
    </a>
</li>
```

### 3.4 Positionner l'article

- Les articles les plus récents doivent être **en haut** de la liste
- Glissez-déposez votre `<li>` pour le positionner correctement dans la vue Tree

### 3.5 Sauvegarder index.html

1. **Ctrl+S** (Windows) ou **Cmd+S** (Mac)
2. Le script `auto-dataset-generator.js` détectera automatiquement le nouveau lien !

---

## Étape 4 : Tester votre article

### 4.1 Prévisualiser dans Pinegrow

1. Cliquez sur le bouton **Preview** dans Pinegrow
2. Vérifiez que votre article apparaît dans la colonne appropriée
3. Cliquez sur le lien pour vérifier que la page s'ouvre correctement

### 4.2 Tester dans un navigateur

1. Ouvrez `index.html` dans votre navigateur préféré
2. Localisez votre article dans le plateau d'accueil
3. Cliquez dessus pour vérifier :
   - La page se charge correctement
   - Le contenu s'affiche bien
   - Les liens de navigation fonctionnent
   - Le responsive design fonctionne (testez sur mobile)

### 4.3 Vérifier le dataset automatique

1. Ouvrez la **Console** du navigateur (F12)
2. Tapez : `window.dataSets`
3. Vous devriez voir votre article dans le dataset correspondant !

---

## Checklist finale

Avant de publier, vérifiez :

- [ ] Le fichier de page existe dans `pages/`
- [ ] Le titre, la date et la catégorie sont corrects
- [ ] Le contenu est complet et formaté
- [ ] Le breadcrumb est correct
- [ ] Le lien est ajouté dans la bonne colonne de `index.html`
- [ ] Le lien `href` est correct (chemin relatif : `pages/votre-article.html`)
- [ ] La classe `list-item` et la catégorie sont correctes
- [ ] L'article apparaît dans le plateau d'accueil
- [ ] Le clic sur le lien ouvre la bonne page
- [ ] La page est responsive (testez sur mobile)
- [ ] Les liens de navigation fonctionnent

---

## Astuces Pinegrow

### Navigation rapide
- **Ctrl+P** : Ouvrir rapidement un fichier
- **Ctrl+F** : Rechercher dans le code
- **Vue Tree** : Naviguer dans la structure HTML

### Édition rapide
- **Double-clic** sur un élément : Éditer le texte
- **Panneau Properties** : Modifier attributs et classes
- **Glisser-déposer** : Réorganiser les éléments

### Multi-pages
- Pinegrow détecte automatiquement les includes (`header`, `nav`, `footer`)
- Si vous modifiez un include, toutes les pages seront mises à jour

### Live preview
- Activez le mode **Live preview** pour voir les changements en temps réel
- Testez le responsive avec les boutons de taille d'écran

---

## Catégories disponibles

Voici les catégories et leurs classes correspondantes :

| Catégorie | Classe à utiliser | ID de liste |
|-----------|-------------------|-------------|
| Généralités - Contributions | `generalites-contrib` | `list-generalites-contrib` |
| Généralités - Documents utiles | `generalites-docs` | `list-generalites-docs` |
| Féminisation - Contributions | `feminisation-contrib` | `list-feminisation-contrib` |
| Féminisation - Documents utiles | `feminisation-docs` | `list-feminisation-docs` |
| Qui est G & S | `qui` | `list-qui` |
| Pour mandataires | `pour-mandataires` | `list-pour-mandataires` |
| Pour Sociétés | `pour-societes` | `list-pour-societes` |

---

## Dépannage

### Mon article n'apparaît pas dans le plateau d'accueil

- Vérifiez que le `<li>` a bien la classe `list-item` et la catégorie
- Vérifiez que le lien `<a>` a bien la classe `item-link`
- Vérifiez que vous avez sauvegardé `index.html`
- Rechargez complètement la page (Ctrl+F5)

### Le lien ne fonctionne pas

- Vérifiez le chemin relatif : doit être `pages/nom-fichier.html`
- Vérifiez que le nom du fichier correspond exactement (respect de la casse)
- Vérifiez que le fichier existe bien dans le dossier `pages/`

### Le style ne s'applique pas

- Vérifiez que les liens CSS sont présents dans le `<head>`
- Vérifiez que vous avez copié les classes Bootstrap correctement
- Rechargez les CSS (Ctrl+F5)

### Le dataset ne se met pas à jour

- Vérifiez que le script `js/auto-dataset-generator.js` est chargé
- Ouvrez la console (F12) et cherchez des erreurs JavaScript
- Vérifiez la structure HTML du lien (doit avoir `item-link` et un `<span>`)

---

## Pour aller plus loin

### Marquer un article "En construction"

Ajoutez la classe `construction` au `<li>` ou au `<a>` :

```html
<li class="list-item generalites-contrib construction">
    <a class="item-link" href="#">
        <span>Article en construction</span>
    </a>
</li>
```

Ou utilisez `href="#"` pour un lien désactivé.

### Ajouter une image à votre article

Dans Pinegrow, dans la zone de contenu :

1. Ajoutez un élément `<img>` depuis la Library
2. Définissez l'attribut `src` : `../images/votre-image.jpg`
3. Ajoutez les classes Bootstrap : `img-fluid rounded`

```html
<img src="../images/votre-image.jpg" class="img-fluid rounded mb-4" alt="Description">
```

### Créer des sections avec des onglets ou accordéons

Utilisez les composants Bootstrap depuis la **Library** de Pinegrow :
- **Accordion** : Sections pliables
- **Tabs** : Navigation par onglets
- **Cards** : Blocs de contenu stylisés

---

## Support

Pour toute question ou problème :
- Consultez la documentation de Pinegrow : https://pinegrow.com/docs/
- Vérifiez que votre version de Pinegrow est à jour
- Testez dans plusieurs navigateurs

---

**Date de création du guide :** 14 octobre 2025
**Version :** 1.0

