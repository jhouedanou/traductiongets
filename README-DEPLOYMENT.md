# 📦 Déploiement sur GitHub Pages

Ce dépôt est publié directement sur **GitHub Pages** depuis la branche `main`.

---

## ✅ Fonctionnement

Le site est servi directement depuis la branche `main` (dossier racine).
À chaque `git push` sur `main`, GitHub Pages republie le contenu statique.

---

## 🚀 Mise en place

1. Ouvrir **Settings** → **Pages** dans le dépôt GitHub
2. Dans **Build and deployment > Source**, sélectionner **Deploy from a branch**
3. Sélectionner la branche **main** et le dossier **/(root)** puis enregistrer
4. Pousser une modification sur `main`

---

## 📁 Fichiers concernés

```
.nojekyll
README-DEPLOYMENT.md
QUICK-START-GITHUB.md
```

---

## ⚠️ Notes importantes

- GitHub Pages ne sert que du **contenu statique**
- Le dossier `backend/` est dans le dépôt mais n'est pas utilisable en hébergement GitHub Pages (statique uniquement)
- Les règles Apache de `.htaccess` ne s'appliquent pas sur GitHub Pages

---

## 🆘 Dépannage

Si le site ne se publie pas :
1. vérifier que **Pages** utilise **Deploy from a branch**
2. vérifier que la branche **main** et le dossier **/(root)** sont sélectionnés
3. attendre quelques minutes puis recharger l'URL GitHub Pages

---

**Dernière mise à jour** : 1 juin 2026
