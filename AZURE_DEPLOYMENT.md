# ☁️ Déploiement sur Azure - ENSPD LearnAI

Guide complet pour déployer l'application sur Microsoft Azure.

## 📋 Prérequis

- Azure CLI installé et configuré ✅
- Compte Azure actif
- Abonnement Azure (gratuit ou payant)

## 🎯 Architecture Azure

Nous allons utiliser :
- **Azure App Service** : Pour héberger l'application Flask
- **Azure Database for PostgreSQL** : Pour la base de données
- **Azure Static Web Apps** (optionnel) : Pour le frontend

---

## 🗄️ Étape 1 : Créer la base de données PostgreSQL

### Via Azure CLI

```bash
# Créer un groupe de ressources
az group create --name learnai-rg --location westeurope

# Créer un serveur PostgreSQL
az postgres flexible-server create \
  --resource-group learnai-rg \
  --name learnai-db-server \
  --location westeurope \
  --admin-user learnai_admin \
  --admin-password VotreMotDePasseSecurise123! \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 14 \
  --storage-size 32 \
  --public-access 0.0.0.0

# Créer la base de données
az postgres flexible-server db create \
  --resource-group learnai-rg \
  --server-name learnai-db-server \
  --database-name learnai

# Configurer le pare-feu pour autoriser les services Azure
az postgres flexible-server firewall-rule create \
  --resource-group learnai-rg \
  --name learnai-db-server \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

### Via le portail Azure

1. Allez sur [portal.azure.com](https://portal.azure.com)
2. Créez une ressource "Azure Database for PostgreSQL"
3. Choisissez "Flexible Server"
4. Configurez :
   - Nom du serveur : `learnai-db-server`
   - Région : West Europe (ou proche de vous)
   - Version : PostgreSQL 14
   - Calcul + stockage : Burstable, B1ms (économique)
   - Admin : `learnai_admin`
   - Mot de passe : Créez un mot de passe fort

---

## 🌐 Étape 2 : Déployer l'application Flask

### Créer l'App Service

```bash
# Créer un plan App Service (Linux)
az appservice plan create \
  --name learnai-plan \
  --resource-group learnai-rg \
  --sku B1 \
  --is-linux

# Créer la Web App
az webapp create \
  --resource-group learnai-rg \
  --plan learnai-plan \
  --name learnai-app \
  --runtime "PYTHON:3.9" \
  --deployment-local-git
```

### Configurer les variables d'environnement

```bash
# Récupérer la chaîne de connexion PostgreSQL
DB_HOST=$(az postgres flexible-server show \
  --resource-group learnai-rg \
  --name learnai-db-server \
  --query "fullyQualifiedDomainName" -o tsv)

# Configurer les variables d'environnement
az webapp config appsettings set \
  --resource-group learnai-rg \
  --name learnai-app \
  --settings \
    DB_NAME=learnai \
    DB_USER=learnai_admin \
    DB_PASSWORD="VotreMotDePasseSecurise123!" \
    DB_HOST=$DB_HOST \
    DB_PORT=5432 \
    GROQ_API_KEY="your-groq-api-key-here" \
    JWT_SECRET_KEY="enspd-learnai-secret-key-2024-secure" \
    SECRET_KEY="enspd-flask-secret-key-2024" \
    DEBUG=False \
    SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

### Déployer le code

```bash
# Ajouter le remote Azure
az webapp deployment source config-local-git \
  --name learnai-app \
  --resource-group learnai-rg

# Récupérer l'URL Git
AZURE_GIT_URL=$(az webapp deployment source show \
  --name learnai-app \
  --resource-group learnai-rg \
  --query "repoUrl" -o tsv)

# Ajouter le remote et pousser
git remote add azure $AZURE_GIT_URL
git push azure main
```

---

## 📦 Étape 3 : Configuration du démarrage

Azure doit savoir comment démarrer l'application Flask.

### Créer un fichier startup.sh

```bash
# startup.sh
cd backend
gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app
```

### Configurer la commande de démarrage

```bash
az webapp config set \
  --resource-group learnai-rg \
  --name learnai-app \
  --startup-file "startup.sh"
```

---

## 🗃️ Étape 4 : Initialiser la base de données

### Se connecter à PostgreSQL

```bash
# Installer psql si nécessaire
# Windows: choco install postgresql
# Mac: brew install postgresql
# Linux: sudo apt install postgresql-client

# Se connecter
psql "host=learnai-db-server.postgres.database.azure.com port=5432 dbname=learnai user=learnai_admin password=VotreMotDePasseSecurise123! sslmode=require"
```

### Exécuter le schéma

```sql
-- Copier-coller le contenu de database/schema.sql
-- Ou depuis le terminal :
\i database/schema.sql
```

### Initialiser les données de test

Depuis votre machine locale, modifiez temporairement `backend/config.py` pour pointer vers Azure, puis :

```bash
cd backend
python scripts/init_db.py
```

---

## 🌍 Étape 5 : Déployer le frontend (optionnel)

### Option A : Avec l'App Service (même domaine)

Le frontend est déjà inclus dans le déploiement. Configurez Flask pour servir les fichiers statiques.

### Option B : Azure Static Web Apps (recommandé)

```bash
# Créer une Static Web App
az staticwebapp create \
  --name learnai-frontend \
  --resource-group learnai-rg \
  --source https://github.com/Junior620/learnAI \
  --location westeurope \
  --branch main \
  --app-location "frontend" \
  --api-location "" \
  --output-location ""
```

Puis mettez à jour les URLs API dans le frontend :

```javascript
// frontend/js/auth.js et autres
const API_URL = 'https://learnai-app.azurewebsites.net/api';
```

---

## 🔍 Étape 6 : Vérification et tests

### Vérifier le déploiement

```bash
# Voir les logs
az webapp log tail \
  --resource-group learnai-rg \
  --name learnai-app

# Ouvrir l'application
az webapp browse \
  --resource-group learnai-rg \
  --name learnai-app
```

### URLs de l'application

- **Backend API** : `https://learnai-app.azurewebsites.net`
- **Frontend** : `https://learnai-app.azurewebsites.net` (si servi par Flask)
- **Frontend Static** : `https://learnai-frontend.azurestaticapps.net` (si Static Web App)

---

## 💰 Coûts estimés

### Configuration économique (recommandée pour débuter)

- **App Service B1** : ~13€/mois
- **PostgreSQL Flexible Server B1ms** : ~12€/mois
- **Static Web Apps** : Gratuit
- **Total** : ~25€/mois

### Configuration gratuite (limitée)

- **App Service F1** : Gratuit (limitations : 60 min/jour, 1 GB RAM)
- **PostgreSQL** : Pas de tier gratuit (minimum ~12€/mois)
- **Static Web Apps** : Gratuit

**Note** : Azure offre 200$ de crédit gratuit pour les nouveaux comptes pendant 30 jours.

---

## 🔧 Commandes utiles

### Redémarrer l'application

```bash
az webapp restart \
  --resource-group learnai-rg \
  --name learnai-app
```

### Voir les logs en temps réel

```bash
az webapp log tail \
  --resource-group learnai-rg \
  --name learnai-app
```

### Mettre à jour les variables d'environnement

```bash
az webapp config appsettings set \
  --resource-group learnai-rg \
  --name learnai-app \
  --settings NOUVELLE_VARIABLE="valeur"
```

### Supprimer toutes les ressources

```bash
az group delete --name learnai-rg --yes --no-wait
```

---

## 🐛 Dépannage

### L'application ne démarre pas

1. Vérifiez les logs : `az webapp log tail`
2. Vérifiez que `startup.sh` est exécutable
3. Vérifiez que toutes les variables d'environnement sont définies

### Erreur de connexion à la base de données

1. Vérifiez les règles de pare-feu PostgreSQL
2. Vérifiez que SSL est activé : `sslmode=require`
3. Testez la connexion depuis votre machine locale

### Le frontend ne se connecte pas au backend

1. Vérifiez les URLs dans le code JavaScript
2. Vérifiez la configuration CORS dans Flask
3. Vérifiez que l'App Service est accessible publiquement

---

## 📚 Ressources

- [Documentation Azure App Service](https://docs.microsoft.com/azure/app-service/)
- [Documentation Azure PostgreSQL](https://docs.microsoft.com/azure/postgresql/)
- [Azure CLI Reference](https://docs.microsoft.com/cli/azure/)

---

## ✅ Checklist de déploiement

- [ ] Groupe de ressources créé
- [ ] Base de données PostgreSQL créée
- [ ] Règles de pare-feu configurées
- [ ] App Service créé
- [ ] Variables d'environnement configurées
- [ ] Code déployé via Git
- [ ] Schéma de base de données exécuté
- [ ] Données de test initialisées
- [ ] URLs frontend mises à jour
- [ ] Application testée et fonctionnelle

Bon déploiement sur Azure ! ☁️
