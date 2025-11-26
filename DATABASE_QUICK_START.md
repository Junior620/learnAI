# 🚀 Quick Start - Base de Données

## En 5 Minutes

### 1️⃣ Créer la Base de Données sur Render

1. Va sur https://dashboard.render.com
2. "New +" → "PostgreSQL"
3. Name: `learnai-db`, Region: Frankfurt, Plan: Free
4. "Create Database"
5. Copie l'**Internal Database URL**

### 2️⃣ Configurer sur Render

1. Va sur ton service "learnai-app"
2. "Environment" → "Add Environment Variable"
3. Colle l'URL:
   ```
   DATABASE_URL = postgresql://user:pass@host:5432/learnai
   ```
4. "Save Changes"

**✅ C'est tout!** L'app va redémarrer et créer automatiquement toutes les tables.

---

## 📊 Migrer tes Données Locales

### Étape 1: Exporter

```bash
cd backend
python export_data.py
```

→ Crée `database_export.json`

### Étape 2: Configurer

Crée `backend/.env`:
```env
DB_HOST=dpg-xxxxx.frankfurt-postgres.render.com
DB_NAME=learnai
DB_USER=learnai_user
DB_PASSWORD=ton_password_render
DB_PORT=5432
```

### Étape 3: Importer

```bash
cd backend
python import_data.py
```

**✅ Terminé!** Tes données sont maintenant sur le serveur.

---

## 🔄 Synchronisation Rapide

Double-clique sur `sync_database.bat` pour synchroniser en un clic!

---

## 📖 Guide Complet

Pour plus de détails, voir: `DATABASE_MIGRATION_GUIDE.md`
