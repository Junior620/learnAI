# 🗄️ Guide de Migration de Base de Données

## Vue d'ensemble

Ce guide explique comment:
1. Créer une base de données PostgreSQL sur Render
2. Initialiser automatiquement les tables
3. Exporter tes données locales
4. Importer tes données sur le serveur

---

## Étape 1: Créer la Base de Données sur Render

### 1.1 Créer la Database

1. Va sur https://dashboard.render.com
2. Clique sur "New +" → "PostgreSQL"
3. Remplis:
   - **Name:** `learnai-db`
   - **Database:** `learnai`
   - **User:** `learnai_user`
   - **Region:** Frankfurt (même que ton app)
   - **PostgreSQL Version:** 16
   - **Plan:** Free
4. Clique sur "Create Database"
5. Attends 2-3 minutes

### 1.2 Récupérer les Informations de Connexion

Une fois créée, tu verras:
- **Internal Database URL** (commence par `postgresql://...`)
- **Hostname**
- **Port**
- **Database**
- **Username**
- **Password**

**⚠️ Important:** Copie l'**Internal Database URL** (pas l'External)

---

## Étape 2: Configurer les Variables d'Environnement

### 2.1 Sur Render (Service Web)

1. Va sur ton service "learnai-app"
2. Clique sur "Environment" (menu gauche)
3. Ajoute ces variables:

**Option A: URL Complète (Recommandé)**
```
DATABASE_URL = postgresql://learnai_user:password@dpg-xxxxx.frankfurt-postgres.render.com:5432/learnai
```

**Option B: Variables Séparées**
```
DB_HOST = dpg-xxxxx.frankfurt-postgres.render.com
DB_NAME = learnai
DB_USER = learnai_user
DB_PASSWORD = [le mot de passe de la DB]
DB_PORT = 5432
```

4. Clique sur "Save Changes"
5. L'app va redémarrer automatiquement

### 2.2 Vérifier l'Initialisation

Après le redémarrage, vérifie les logs:
```
Dashboard → Logs
```

Tu devrais voir:
```
🔄 Première exécution - Initialisation de la base de données...
✅ Base de données initialisée avec succès!
📊 Tables créées: users, student_profiles, subjects, grades, ...
```

---

## Étape 3: Exporter tes Données Locales

### 3.1 Vérifier la Configuration Locale

Ouvre `backend/export_data.py` et vérifie que les infos correspondent à ta BD locale:
```python
LOCAL_DB_CONFIG = {
    'host': 'localhost',
    'database': 'learnai',
    'user': 'postgres',
    'password': 'kidjamo@',  # ← Vérifie ton mot de passe
    'port': 5432
}
```

### 3.2 Exécuter l'Export

```bash
cd backend
python export_data.py
```

**Résultat attendu:**
```
🔄 Connexion à la base de données locale...
📊 Export de users...
   ✅ 5 lignes exportées
📊 Export de student_profiles...
   ✅ 3 lignes exportées
...
✅ Export terminé!
📁 Fichier: database_export.json
📊 Total: 42 lignes exportées
```

Un fichier `database_export.json` sera créé dans le dossier `backend/`.

---

## Étape 4: Importer les Données sur le Serveur

### 4.1 Configurer les Variables Localement

Crée un fichier `.env` dans le dossier `backend/` avec les infos de ta BD Render:

```env
DB_HOST=dpg-xxxxx.frankfurt-postgres.render.com
DB_NAME=learnai
DB_USER=learnai_user
DB_PASSWORD=ton_mot_de_passe_render
DB_PORT=5432
```

### 4.2 Exécuter l'Import

```bash
cd backend
python import_data.py
```

**Résultat attendu:**
```
🔄 Import des données vers la base de production...
✅ Connecté à dpg-xxxxx.frankfurt-postgres.render.com
📅 Export du: 2025-11-25T...
📊 Tables à importer: 10

📊 Import de users...
   ✅ 5 lignes importées
📊 Import de student_profiles...
   ✅ 3 lignes importées
...
🔄 Mise à jour des séquences...
✅ Import terminé!
📊 Total: 42 lignes importées
```

---

## Étape 5: Vérifier l'Import

### 5.1 Via l'API

Teste la connexion à l'API:
```bash
curl https://learnai-2dnf.onrender.com/api/auth/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"ton_email@test.com","password":"ton_password"}'
```

### 5.2 Via Render Dashboard

1. Va sur ta database "learnai-db"
2. Clique sur "Connect" → "External Connection"
3. Utilise un client PostgreSQL (pgAdmin, DBeaver, etc.)
4. Vérifie que les tables contiennent tes données

---

## 🔄 Synchronisation Continue

### Option 1: Export/Import Manuel

Quand tu veux synchroniser:
```bash
# 1. Exporter les données locales
cd backend
python export_data.py

# 2. Importer sur le serveur
python import_data.py
```

### Option 2: Script Automatisé

Crée un script `sync_database.bat`:
```batch
@echo off
cd backend
echo Exporting local data...
python export_data.py
echo.
echo Importing to production...
python import_data.py
echo.
echo Done!
pause
```

Double-clique dessus pour synchroniser en un clic!

---

## 📊 Structure des Fichiers

```
backend/
├── init_db.py              # Initialisation auto au démarrage
├── export_data.py          # Export données locales → JSON
├── import_data.py          # Import JSON → serveur
└── database_export.json    # Fichier de données exportées
```

---

## ⚠️ Notes Importantes

### Sécurité
- ⚠️ **NE JAMAIS** commiter `database_export.json` sur GitHub (contient des données sensibles)
- ⚠️ **NE JAMAIS** commiter le fichier `.env` avec les mots de passe
- ✅ Ces fichiers sont déjà dans `.gitignore`

### Mots de Passe
- Les mots de passe dans `database_export.json` sont déjà hashés (bcrypt)
- Ils peuvent être importés directement sans re-hashage

### Conflits
- L'import utilise `ON CONFLICT DO NOTHING`
- Les données existantes ne seront pas écrasées
- Seules les nouvelles données seront ajoutées

---

## 🆘 Dépannage

### "Variables de base de données non configurées"
→ Vérifie que DB_HOST, DB_NAME, etc. sont bien définis sur Render

### "Erreur de connexion à la base de données"
→ Vérifie que tu utilises l'**Internal Database URL**, pas l'External
→ Vérifie que la DB et l'app sont dans la même région (Frankfurt)

### "Fichier database_export.json non trouvé"
→ Exécute d'abord `python export_data.py` depuis le dossier `backend/`

### "Permission denied"
→ Vérifie les credentials de la base de données
→ Vérifie que l'utilisateur a les droits INSERT

---

## ✅ Checklist Complète

- [ ] Base de données PostgreSQL créée sur Render
- [ ] Variables d'environnement configurées sur Render
- [ ] App redémarrée et logs vérifiés
- [ ] Tables créées automatiquement
- [ ] Données locales exportées (`database_export.json` créé)
- [ ] Fichier `.env` local créé avec infos Render
- [ ] Données importées sur le serveur
- [ ] Import vérifié via API ou client PostgreSQL

**Félicitations! Ta base de données est maintenant synchronisée! 🎉**
