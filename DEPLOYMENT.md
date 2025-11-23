# 🚀 Guide de Déploiement

## Déploiement sur Vercel

### ⚠️ Limitations importantes

Vercel est excellent pour les applications serverless, mais il y a des contraintes :

1. **Base de données** : PostgreSQL local ne fonctionnera pas. Il faut utiliser une base de données cloud comme :
   - **Supabase** (PostgreSQL gratuit)
   - **Neon** (PostgreSQL serverless)
   - **Railway** (PostgreSQL avec plan gratuit)
   - **ElephantSQL** (PostgreSQL gratuit limité)

2. **Timeout** : Les fonctions serverless ont un timeout de 10 secondes (plan gratuit) ou 60 secondes (plan pro)

3. **Stockage** : Pas de stockage persistant sur le serveur

### 📋 Étapes de déploiement

#### 1. Préparer la base de données cloud

**Option A : Supabase (Recommandé)**

1. Créez un compte sur [supabase.com](https://supabase.com)
2. Créez un nouveau projet
3. Allez dans Settings > Database
4. Copiez la "Connection string" (mode "Session")
5. Exécutez le script `database/schema.sql` dans l'éditeur SQL de Supabase

**Option B : Neon**

1. Créez un compte sur [neon.tech](https://neon.tech)
2. Créez un nouveau projet
3. Copiez la connection string
4. Utilisez un client PostgreSQL pour exécuter `database/schema.sql`

#### 2. Installer Vercel CLI

```bash
npm install -g vercel
```

#### 3. Configurer les variables d'environnement

Dans le dashboard Vercel ou via CLI :

```bash
vercel env add DB_NAME
vercel env add DB_USER
vercel env add DB_PASSWORD
vercel env add DB_HOST
vercel env add DB_PORT
vercel env add GROQ_API_KEY
vercel env add JWT_SECRET_KEY
vercel env add SECRET_KEY
```

Ou créez un fichier `.env.production` (ne pas commit) :

```env
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_cloud_db_host
DB_PORT=5432
GROQ_API_KEY=your_groq_key
JWT_SECRET_KEY=your_jwt_secret
SECRET_KEY=your_flask_secret
DEBUG=False
```

#### 4. Modifier le fichier config.py

Le fichier est déjà configuré pour utiliser les variables d'environnement.

#### 5. Déployer sur Vercel

```bash
# Se connecter à Vercel
vercel login

# Déployer
vercel --prod
```

Ou via GitHub :

1. Connectez votre repo GitHub à Vercel
2. Vercel détectera automatiquement le projet
3. Ajoutez les variables d'environnement dans le dashboard
4. Déployez !

#### 6. Mettre à jour les URLs dans le frontend

Dans tous les fichiers JavaScript du frontend, remplacez :

```javascript
// Avant
const API_URL = 'http://localhost:5000/api';

// Après
const API_URL = 'https://votre-app.vercel.app/api';
```

Ou mieux, utilisez une variable d'environnement :

```javascript
const API_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:5000/api'
  : 'https://votre-app.vercel.app/api';
```

---

## Alternative : Déploiement sur Railway (Plus simple)

Railway supporte mieux les applications avec base de données.

### Avantages de Railway

- Base de données PostgreSQL incluse
- Pas de timeout strict
- Configuration plus simple
- Plan gratuit généreux

### Étapes

1. Créez un compte sur [railway.app](https://railway.app)
2. Créez un nouveau projet
3. Ajoutez PostgreSQL depuis le marketplace
4. Déployez depuis GitHub
5. Railway détectera automatiquement Python et installera les dépendances
6. Ajoutez les variables d'environnement
7. Votre app sera en ligne !

---

## Alternative : Déploiement sur Render

### Avantages de Render

- Base de données PostgreSQL gratuite
- Déploiement automatique depuis GitHub
- SSL gratuit
- Bon pour les applications full-stack

### Étapes

1. Créez un compte sur [render.com](https://render.com)
2. Créez une nouvelle "Web Service"
3. Connectez votre repo GitHub
4. Configurez :
   - Build Command : `pip install -r backend/requirements.txt`
   - Start Command : `cd backend && python app.py`
5. Créez une base de données PostgreSQL
6. Ajoutez les variables d'environnement
7. Déployez !

---

## Recommandation finale

Pour ce projet, je recommande **Railway** ou **Render** plutôt que Vercel car :

- ✅ Base de données PostgreSQL incluse
- ✅ Pas de contraintes serverless
- ✅ Configuration plus simple
- ✅ Meilleur pour les applications Flask traditionnelles

Vercel est excellent pour Next.js et les APIs serverless simples, mais moins adapté pour une application Flask avec base de données relationnelle.

---

## 🔧 Fichiers de configuration créés

- `vercel.json` : Configuration Vercel (si vous choisissez Vercel)
- `backend/api/index.py` : Point d'entrée serverless
- Ce guide de déploiement

---

## 📝 Checklist avant déploiement

- [ ] Base de données cloud configurée
- [ ] Variables d'environnement définies
- [ ] Script `schema.sql` exécuté sur la BDD cloud
- [ ] Script `init_db.py` exécuté pour les données de test
- [ ] URLs API mises à jour dans le frontend
- [ ] Tests effectués en local avec la BDD cloud
- [ ] `.env` ajouté au `.gitignore` (déjà fait)
- [ ] Clés API sécurisées (déjà fait)

Bon déploiement ! 🚀
