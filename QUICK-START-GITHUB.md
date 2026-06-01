# 🚀 Guide Rapide : Déploiement Automatique GitHub → OVH

## ⚡ Configuration en 3 étapes (5 minutes)

### 1️⃣ Pousser le code sur GitHub

```bash
# Si ce n'est pas déjà fait
git add .
git commit -m "Setup automated FTP deployment"
git push origin main
```

### 2️⃣ Configurer les Secrets GitHub

**Sur GitHub** : `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

Ajoutez ces 4 secrets :

```
FTP_HOST      → ftp.cluster002.hosting.ovh.net
FTP_USER      → gets
FTP_PASSWORD  → Hs9Txr5H4
FTP_PATH      → /
```

### 3️⃣ C'est tout ! 🎉

Le déploiement est maintenant automatique à chaque `git push` !

---

## 📺 Voir vos déploiements

**GitHub** → Onglet `Actions` → Workflow "Deploy to OVH via FTP"

---

## 🔄 Workflow quotidien

```bash
# 1. Modifier vos fichiers
# 2. Commiter
git add .
git commit -m "Mise à jour du contenu"

# 3. Pousser
git push origin main

# ✨ Déploiement automatique sur OVH !
```

---

## 📚 Documentation complète

Voir [GITHUB-ACTIONS-SETUP.md](GITHUB-ACTIONS-SETUP.md) pour :
- Dépannage
- Déploiement manuel
- Options avancées
- Notifications

---

## ⚠️ IMPORTANT : Sécurité

Le fichier `deploy-ftp.sh` contient vos identifiants FTP en clair.
Il est maintenant dans `.gitignore` et ne sera **jamais** poussé sur GitHub.

✅ GitHub Actions utilise des secrets chiffrés (sécurisé)
❌ Ne commitez jamais `deploy-ftp.sh` (dangereux)

---

## 💡 Astuce

Pour vérifier que `deploy-ftp.sh` n'est pas tracké :

```bash
git status
# deploy-ftp.sh ne doit PAS apparaître
```

Si il apparaît, supprimez-le du tracking :

```bash
git rm --cached deploy-ftp.sh
git commit -m "Remove sensitive file from tracking"
git push
```
