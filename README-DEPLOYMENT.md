# 📦 Système de Déploiement G-ET-S

Ce projet dispose de **deux méthodes de déploiement** pour pousser vos modifications sur le serveur OVH.

---

## 🎯 Méthode Recommandée : GitHub Actions (Automatique & Sécurisé)

### ✅ Avantages
- 🔒 **100% sécurisé** : Identifiants chiffrés dans GitHub Secrets
- ⚡ **Automatique** : Déploie à chaque `git push`
- 📊 **Traçable** : Historique complet des déploiements
- 👥 **Collaboratif** : Une seule configuration pour toute l'équipe

### 🚀 Démarrage rapide
Voir [QUICK-START-GITHUB.md](QUICK-START-GITHUB.md) (5 minutes de configuration)

### 📚 Documentation complète
Voir [GITHUB-ACTIONS-SETUP.md](GITHUB-ACTIONS-SETUP.md)

---

## 🛠️ Méthode Alternative : Script Local (Manuel)

### ⚠️ Attention
Cette méthode contient les identifiants FTP **en clair** dans le script.
**Ne commitez jamais `deploy-ftp.sh` sur GitHub !**

### Utilisation
```bash
./deploy-ftp.sh
```

### 📚 Documentation
Voir [DEPLOIEMENT-FTP.md](DEPLOIEMENT-FTP.md)

---

## 🔀 Quelle méthode choisir ?

| Critère | GitHub Actions | Script Local |
|---------|----------------|--------------|
| **Sécurité** | ✅ Excellente | ⚠️ À risque |
| **Simplicité** | ✅ Automatique | ⚠️ Manuel |
| **Configuration** | ⚡ Une fois | ❌ Sur chaque machine |
| **Recommandé pour** | Production | Développement/Tests |

---

## 📁 Fichiers du système de déploiement

```
MigrationGetS/
├── .github/
│   └── workflows/
│       └── deploy-ftp.yml           # Workflow GitHub Actions
├── .git-ftp-ignore                  # Fichiers exclus du déploiement
├── .gitignore                       # Fichiers exclus de Git (dont deploy-ftp.sh)
├── deploy-ftp.sh                    # Script de déploiement local (⚠️ SENSIBLE)
├── DEPLOIEMENT-FTP.md               # Doc script local
├── GITHUB-ACTIONS-SETUP.md          # Doc GitHub Actions (complète)
├── QUICK-START-GITHUB.md            # Guide rapide GitHub Actions
└── README-DEPLOYMENT.md             # Ce fichier
```

---

## 🔐 Sécurité

### ✅ Bonnes pratiques appliquées

1. **`.gitignore` configuré** pour exclure :
   - `deploy-ftp.sh` (contient identifiants)
   - `.env` et fichiers de configuration
   - Logs et fichiers temporaires

2. **GitHub Secrets** pour stocker :
   - FTP_HOST
   - FTP_USER
   - FTP_PASSWORD
   - FTP_PATH

3. **`.git-ftp-ignore`** pour exclure du déploiement :
   - Fichiers Git
   - Documentation
   - Scripts de déploiement
   - Fichiers de développement

### ⚠️ Vérification rapide

```bash
# Vérifier que deploy-ftp.sh n'est pas tracké
git status

# deploy-ftp.sh ne doit PAS apparaître dans les fichiers modifiés
```

Si il apparaît :
```bash
git rm --cached deploy-ftp.sh
git commit -m "Remove sensitive file"
```

---

## 🆘 Support

### GitHub Actions ne fonctionne pas ?
1. Vérifiez que les 4 secrets sont configurés dans GitHub
2. Consultez les logs dans l'onglet Actions
3. Voir [GITHUB-ACTIONS-SETUP.md](GITHUB-ACTIONS-SETUP.md) section "Dépannage"

### Script local ne fonctionne pas ?
1. Vérifiez que le script est exécutable : `chmod +x deploy-ftp.sh`
2. Vérifiez votre connexion internet
3. Voir [DEPLOIEMENT-FTP.md](DEPLOIEMENT-FTP.md) section "Dépannage"

---

## 🎓 Ressources

- **Documentation GitHub Actions** : https://docs.github.com/actions
- **Documentation git-ftp** : https://github.com/git-ftp/git-ftp
- **Support OVH** : https://www.ovh.com/fr/support/

---

## 📝 Notes importantes

1. **Ne jamais commiter d'identifiants** dans le code source
2. **Utiliser GitHub Actions** en production
3. **Le script local** est uniquement pour tests/développement
4. **Vérifier `.gitignore`** régulièrement

---

**Dernière mise à jour** : 20 octobre 2025
**Version** : 1.0
