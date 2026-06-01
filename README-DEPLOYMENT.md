# 📦 Déploiement sur GitHub Pages

Ce dépôt est maintenant déployé automatiquement sur **GitHub Pages**.

---

## ✅ Fonctionnement

Le site est publié automatiquement :
- à chaque `git push` sur `main`
- ou manuellement depuis l'onglet **Actions** avec `workflow_dispatch`

Le workflow :
- récupère le dépôt
- prépare une copie statique du site
- exclut les fichiers non publics et le dossier `backend/`
- publie le résultat sur GitHub Pages

---

## 🚀 Mise en place

1. Ouvrir **Settings** → **Pages** dans le dépôt GitHub
2. Dans **Source**, sélectionner **GitHub Actions**
3. Pousser une modification sur `main` ou lancer le workflow manuellement

---

## 📁 Fichiers concernés

```
.github/workflows/deploy-github-pages.yml
.nojekyll
README-DEPLOYMENT.md
QUICK-START-GITHUB.md
```

---

## ⚠️ Notes importantes

- GitHub Pages ne sert que du **contenu statique**
- Le dossier `backend/` n'est pas publié
- Les fichiers Markdown de documentation ne sont pas publiés
- Les règles Apache de `.htaccess` ne s'appliquent pas sur GitHub Pages

---

## 🆘 Dépannage

Si le site ne se publie pas :
1. vérifier que **GitHub Actions** est autorisé dans les paramètres du dépôt
2. vérifier que **Pages** utilise bien **GitHub Actions** comme source
3. consulter les logs du workflow dans l'onglet **Actions**

---

**Dernière mise à jour** : 1 juin 2026
