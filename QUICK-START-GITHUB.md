# 🚀 Guide rapide : déploiement vers GitHub Pages

## Configuration en 3 étapes

### 1️⃣ Activer GitHub Pages

Sur GitHub : **Settings** → **Pages** → **Build and deployment** :
- **Source** : `Deploy from a branch`
- **Branch** : `main`
- **Folder** : `/(root)`

### 2️⃣ Pousser le code

```bash
git add .
git commit -m "Configure GitHub Pages deployment"
git push origin main
```

### 3️⃣ Vérifier le déploiement

- Ouvrir **Settings** → **Pages**
- Vérifier le message de publication GitHub Pages
- Ouvrir l'URL du site

---

## 🔄 Workflow quotidien

```bash
# 1. Modifier les fichiers du site
# 2. Commiter
git add .
git commit -m "Mise à jour du site"

# 3. Pousser
git push origin main
```

La publication GitHub Pages se met à jour automatiquement.

---

## ⚠️ Limites à garder en tête

- GitHub Pages héberge uniquement du contenu statique
- Le site doit rester statique pour être compatible GitHub Pages

---

## 🆘 En cas de problème

1. vérifier que **Pages** utilise **Deploy from a branch**
2. vérifier la branche `main` et le dossier `/(root)`
3. attendre quelques minutes après le push puis recharger la page
