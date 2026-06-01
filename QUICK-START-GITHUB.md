# 🚀 Guide rapide : déploiement vers GitHub Pages

## Configuration en 3 étapes

### 1️⃣ Activer GitHub Pages

Sur GitHub : **Settings** → **Pages** → **Source** → **GitHub Actions**

### 2️⃣ Pousser le code

```bash
git add .
git commit -m "Configure GitHub Pages deployment"
git push origin main
```

### 3️⃣ Vérifier le déploiement

- Ouvrir l'onglet **Actions**
- Attendre le workflow **Deploy to GitHub Pages**
- Ouvrir l'URL publiée dans l'environnement `github-pages`

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

Le déploiement se lance automatiquement.

---

## ⚠️ Limites à garder en tête

- GitHub Pages héberge uniquement du contenu statique
- Le dossier `backend/` n'est pas déployé
- Les fichiers `.md` de documentation ne sont pas publiés

---

## 🆘 En cas de problème

1. vérifier que **Pages** utilise **GitHub Actions** comme source
2. vérifier l'exécution du workflow dans **Actions**
3. relancer le workflow manuellement si nécessaire
