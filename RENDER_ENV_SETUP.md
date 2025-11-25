# Configuration des Variables d'Environnement sur Render

## 🔐 Variables Déjà Configurées (Automatiques)

✅ **SECRET_KEY** - Généré automatiquement par Render
✅ **JWT_SECRET_KEY** - Généré automatiquement par Render  
✅ **DEBUG** - Défini à `False`

---

## 🤖 Activer le Chatbot (Optionnel)

### 1. Obtenir une clé API Groq

1. Va sur https://console.groq.com
2. Crée un compte (gratuit)
3. Va dans "API Keys"
4. Clique sur "Create API Key"
5. Copie la clé (commence par `gsk_...`)

### 2. Ajouter sur Render

1. Va sur https://dashboard.render.com
2. Sélectionne ton service "learnai-app"
3. Clique sur "Environment" dans le menu de gauche
4. Clique sur "Add Environment Variable"
5. Ajoute:
   - **Key:** `GROQ_API_KEY`
   - **Value:** `gsk_...` (ta clé copiée)
6. Clique sur "Save Changes"

L'app va redémarrer automatiquement avec la nouvelle variable.

---

## 🗄️ Ajouter une Base de Données PostgreSQL (Recommandé)

### Pourquoi?
Actuellement, l'app n'a pas de base de données. Les données ne sont pas persistées.

### 1. Créer une Base de Données sur Render

1. Sur Render Dashboard, clique sur "New +" → "PostgreSQL"
2. Remplis:
   - **Name:** `learnai-db`
   - **Database:** `learnai`
   - **User:** `learnai_user`
   - **Region:** Frankfurt (même que ton app)
   - **Plan:** Free
3. Clique sur "Create Database"
4. Attends 2-3 minutes que la base soit créée

### 2. Récupérer les Informations de Connexion

Une fois créée, tu verras:
- **Internal Database URL** (utilise celle-ci)
- **External Database URL**
- **PSQL Command**

Copie l'**Internal Database URL** (commence par `postgresql://...`)

### 3. Ajouter les Variables dans ton Service Web

Retourne sur ton service "learnai-app" → Environment

Ajoute ces variables (Render peut les remplir automatiquement si tu lies la DB):

**Option A: Automatique (Recommandé)**
1. Dans ton service web, va dans "Environment"
2. Clique sur "Add Database"
3. Sélectionne ta base "learnai-db"
4. Render ajoutera automatiquement `DATABASE_URL`

**Option B: Manuel**
Parse l'URL PostgreSQL et ajoute:
```
postgresql://user:password@host:port/database
```

Ajoute séparément:
- **DB_HOST:** `dpg-xxxxx.frankfurt-postgres.render.com`
- **DB_NAME:** `learnai`
- **DB_USER:** `learnai_user`
- **DB_PASSWORD:** `[le mot de passe de la DB]`
- **DB_PORT:** `5432`

### 4. Initialiser la Base de Données

Une fois les variables ajoutées, tu dois créer les tables.

**Via SSH sur Render:**
1. Dans ton service, va dans "Shell"
2. Exécute:
```bash
cd backend
python -c "from database import init_db; init_db()"
```

Ou crée un script d'initialisation dans `backend/scripts/init_db.py`

---

## 🧪 Tester la Configuration

### Test API de Base
```bash
curl https://learnai-2dnf.onrender.com/
```

Devrait retourner:
```json
{
  "message": "ENSPD LearnAI API",
  "version": "1.0.0",
  "status": "running"
}
```

### Test avec Base de Données
```bash
curl https://learnai-2dnf.onrender.com/api/auth/signup \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123","role":"student"}'
```

---

## 📊 Résumé des Variables

| Variable | Status | Requis | Description |
|----------|--------|--------|-------------|
| SECRET_KEY | ✅ Auto | Oui | Clé secrète Flask |
| JWT_SECRET_KEY | ✅ Auto | Oui | Clé JWT |
| DEBUG | ✅ Auto | Oui | Mode debug (False) |
| GROQ_API_KEY | ⚠️ Manuel | Non | Pour le chatbot IA |
| DB_HOST | ⚠️ Manuel | Non* | Hôte PostgreSQL |
| DB_NAME | ⚠️ Manuel | Non* | Nom de la DB |
| DB_USER | ⚠️ Manuel | Non* | Utilisateur DB |
| DB_PASSWORD | ⚠️ Manuel | Non* | Mot de passe DB |
| DB_PORT | ⚠️ Manuel | Non* | Port DB (5432) |

*Non requis mais fortement recommandé pour la production

---

## 🆘 Problèmes Courants

### L'app ne démarre pas après ajout de variables
- Vérifie les logs: Dashboard → Logs
- Les variables sont bien orthographiées?
- Redémarre manuellement: Settings → Manual Deploy

### Erreur de connexion à la base de données
- Utilise l'**Internal Database URL**, pas l'External
- Vérifie que la DB et l'app sont dans la même région
- Vérifie que les variables DB sont correctes

### Le chatbot ne fonctionne pas
- Vérifie que GROQ_API_KEY est bien définie
- Teste la clé sur https://console.groq.com
- Vérifie les logs pour voir les erreurs

---

**Besoin d'aide?** Vérifie les logs sur Render Dashboard → Logs
