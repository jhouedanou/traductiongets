# 📦 Déploiement sur GitHub Pages

Ce dépôt est publié directement sur **GitHub Pages** depuis la branche `main`.

> ⚠️ **Attention sécurité** : en publication depuis `main`, le dossier `backend/` devient publiquement visible. Vérifiez qu'il ne contient aucun secret, identifiant, clé API ou configuration sensible avant de publier.

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
- Le dossier `backend/` reste visible dans le site publié, mais ses endpoints serveur ne fonctionneront pas sur GitHub Pages
- ⚠️ Si `backend/` contient des éléments sensibles, il faut le déplacer hors de la branche publiée (ou le retirer) avant publication
- Le fichier `.nojekyll` reste nécessaire car le dépôt contient des dossiers commençant par `_` (ex. `_pginfo`)
- Les règles Apache de `.htaccess` ne s'appliquent pas sur GitHub Pages

---

## 🆘 Dépannage

Si le site ne se publie pas :
1. vérifier que **Pages** utilise **Deploy from a branch**
2. vérifier que la branche **main** et le dossier **/(root)** sont sélectionnés
3. attendre quelques minutes puis recharger l'URL GitHub Pages

---

**Dernière mise à jour** : 1 juin 2026
