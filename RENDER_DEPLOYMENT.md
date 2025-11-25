# Déploiement sur Render

## Étapes rapides

1. **Créer un compte sur Render**
   - Va sur https://render.com
   - Inscris-toi avec ton compte GitHub

2. **Connecter ton repo GitHub**
   - Dans Render Dashboard, clique sur "New +"
   - Sélectionne "Web Service"
   - Connecte ton repo GitHub `Junior620/learnAI`
   - Render détectera automatiquement le fichier `render.yaml`

3. **Configuration automatique**
   - Render va lire le fichier `render.yaml` et configurer tout automatiquement
   - Les variables d'environnement SECRET_KEY et JWT_SECRET_KEY seront générées automatiquement

4. **Déploiement**
   - Clique sur "Create Web Service"
   - Render va:
     - Installer les dépendances
     - Démarrer l'application
     - Te donner une URL (ex: https://learnai-app.onrender.com)

5. **Variables d'environnement optionnelles**
   Si tu veux utiliser une base de données PostgreSQL ou l'API Groq:
   - Va dans "Environment" dans ton service
   - Ajoute:
     - `DB_HOST` (si tu as une base de données)
     - `DB_NAME`
     - `DB_USER`
     - `DB_PASSWORD`
     - `DB_PORT`
     - `GROQ_API_KEY` (pour le chatbot)

## Avantages de Render

- ✅ Déploiement automatique à chaque push sur GitHub
- ✅ HTTPS gratuit
- ✅ Logs en temps réel
- ✅ Redémarrage automatique en cas d'erreur
- ✅ Plan gratuit suffisant pour commencer

## URL de ton application

Une fois déployé, ton API sera accessible à:
`https://learnai-app.onrender.com`

Tu pourras tester avec:
`https://learnai-app.onrender.com/` → Devrait retourner le message de bienvenue
