#!/bin/bash

# Script de déploiement automatique sur Azure
# ENSPD LearnAI

echo "🚀 Déploiement de ENSPD LearnAI sur Azure"
echo "=========================================="

# Variables
RESOURCE_GROUP="learnai-rg"
LOCATION="westeurope"
DB_SERVER="learnai-db-server"
DB_NAME="learnai"
DB_ADMIN="learnai_admin"
DB_PASSWORD="LearnAI2024Secure!"
APP_NAME="learnai-app"
PLAN_NAME="learnai-plan"

# 1. Créer le groupe de ressources
echo "📦 Création du groupe de ressources..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# 2. Créer le serveur PostgreSQL
echo "🗄️ Création du serveur PostgreSQL..."
az postgres flexible-server create \
  --resource-group $RESOURCE_GROUP \
  --name $DB_SERVER \
  --location $LOCATION \
  --admin-user $DB_ADMIN \
  --admin-password $DB_PASSWORD \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 14 \
  --storage-size 32 \
  --public-access 0.0.0.0

# 3. Créer la base de données
echo "💾 Création de la base de données..."
az postgres flexible-server db create \
  --resource-group $RESOURCE_GROUP \
  --server-name $DB_SERVER \
  --database-name $DB_NAME

# 4. Configurer le pare-feu
echo "🔥 Configuration du pare-feu..."
az postgres flexible-server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --name $DB_SERVER \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# 5. Créer le plan App Service
echo "📱 Création du plan App Service..."
az appservice plan create \
  --name $PLAN_NAME \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux

# 6. Créer la Web App
echo "🌐 Création de la Web App..."
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $PLAN_NAME \
  --name $APP_NAME \
  --runtime "PYTHON:3.9"

# 7. Récupérer l'hôte de la base de données
DB_HOST=$(az postgres flexible-server show \
  --resource-group $RESOURCE_GROUP \
  --name $DB_SERVER \
  --query "fullyQualifiedDomainName" -o tsv)

# 8. Configurer les variables d'environnement
echo "⚙️ Configuration des variables d'environnement..."
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --settings \
    DB_NAME=$DB_NAME \
    DB_USER=$DB_ADMIN \
    DB_PASSWORD=$DB_PASSWORD \
    DB_HOST=$DB_HOST \
    DB_PORT=5432 \
    GROQ_API_KEY="your-groq-api-key-here" \
    JWT_SECRET_KEY="enspd-learnai-secret-key-2024-secure" \
    SECRET_KEY="enspd-flask-secret-key-2024" \
    DEBUG=False \
    SCM_DO_BUILD_DURING_DEPLOYMENT=true

# 9. Configurer la commande de démarrage
echo "🎬 Configuration du démarrage..."
az webapp config set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME \
  --startup-file "startup.sh"

# 10. Configurer le déploiement Git
echo "📤 Configuration du déploiement Git..."
az webapp deployment source config-local-git \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP

# Récupérer l'URL Git
AZURE_GIT_URL=$(az webapp deployment list-publishing-credentials \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query "scmUri" -o tsv)

echo ""
echo "✅ Configuration terminée !"
echo "=========================================="
echo "📊 Informations de déploiement :"
echo "   - Groupe de ressources : $RESOURCE_GROUP"
echo "   - Base de données : $DB_HOST"
echo "   - Application : https://$APP_NAME.azurewebsites.net"
echo ""
echo "📤 Pour déployer le code :"
echo "   git remote add azure <URL_GIT_AZURE>"
echo "   git push azure main"
echo ""
echo "🔍 Pour voir les logs :"
echo "   az webapp log tail --resource-group $RESOURCE_GROUP --name $APP_NAME"
echo ""
