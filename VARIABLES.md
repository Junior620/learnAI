# 🔐 Variables d'environnement - ENSPD LearnAI

Ce document liste toutes les variables d'environnement nécessaires pour faire fonctionner l'application.

## 📋 Variables requises

### Base de données PostgreSQL

| Variable | Valeur par défaut | Description |
|----------|------------------|-------------|
| `DB_NAME` | `learnai` | Nom de la base de données |
| `DB_USER` | `postgres` | Nom d'utilisateur PostgreSQL |
| `DB_PASSWORD` | `your_password_here` | Mot de passe PostgreSQL |
| `DB_HOST` | `localhost` | Hôte de la base de données |
| `DB_PORT` | `5432` | Port PostgreSQL |

### Sécurité et authentification

| Variable | Valeur par défaut | Description |
|----------|------------------|-------------|
| `JWT_SECRET_KEY` | `change-this-secret-key-in-production` | Clé secrète pour les tokens JWT |
| `SECRET_KEY` | `change-this-secret-key-in-production` | Clé secrète Flask |

### API du chatbot (choisir l'une des deux)

| Variable | Valeur par défaut | Description |
|----------|------------------|-------------|
| `GROQ_API_KEY` | *(vide)* | Clé API Groq (recommandé - gratuit et rapide) |
| `GEMINI_API_KEY` | *(vide)* | Clé API Google Gemini (alternative) |

### Configuration générale

| Variable | Valeur par défaut | Description |
|----------|------------------|-------------|
| `DEBUG` | `True` | Mode debug (mettre `False` en production) |

---

## 🚀 Configuration pour le déploiement

### Pour Railway

Ajoutez ces variables dans le dashboard Railway :

```
DB_NAME=learnai
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe_railway
DB_HOST=containers-us-west-xxx.railway.app
DB_PORT=5432
JWT_SECRET_KEY=votre-cle-secrete-jwt-unique
SECRET_KEY=votre-cle-secrete-flask-unique
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx
DEBUG=False
```

### Pour Render

Ajoutez ces variables dans le dashboard Render :

```
DB_NAME=learnai
DB_USER=learnai_user
DB_PASSWORD=votre_mot_de_passe_render
DB_HOST=dpg-xxxxxxxxxxxxx.oregon-postgres.render.com
DB_PORT=5432
JWT_SECRET_KEY=votre-cle-secrete-jwt-unique
SECRET_KEY=votre-cle-secrete-flask-unique
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx
DEBUG=False
```

### Pour Vercel

Ajoutez ces variables dans le dashboard Vercel ou via CLI :

```bash
vercel env add DB_NAME
vercel env add DB_USER
vercel env add DB_PASSWORD
vercel env add DB_HOST
vercel env add DB_PORT
vercel env add JWT_SECRET_KEY
vercel env add SECRET_KEY
vercel env add GROQ_API_KEY
vercel env add DEBUG
```

---

## 🔑 Comment obtenir les clés API

### Groq API (Recommandé)

1. Allez sur [console.groq.com](https://console.groq.com)
2. Créez un compte gratuit
3. Allez dans "API Keys"
4. Créez une nouvelle clé
5. Copiez la clé (format : `gsk_xxxxxxxxxxxxxxxxxxxxx`)

**Avantages :**
- Gratuit
- Très rapide
- Pas de limite stricte
- Modèles puissants (Llama, Mixtral)

### Google Gemini API (Alternative)

1. Allez sur [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Créez un compte Google
3. Créez une nouvelle clé API
4. Copiez la clé (format : `AIzaSyxxxxxxxxxxxxxxxxxxxxx`)

**Avantages :**
- Gratuit (avec limites)
- Modèle Gemini Pro
- Intégration Google

---

## 🔒 Génération de clés secrètes

Pour générer des clés secrètes sécurisées :

### Avec Python

```python
import secrets
print(secrets.token_urlsafe(32))
```

### Avec OpenSSL

```bash
openssl rand -base64 32
```

### En ligne

Utilisez [randomkeygen.com](https://randomkeygen.com/) pour générer des clés aléatoires.

---

## 📝 Fichier .env local

Créez un fichier `.env` à la racine du projet (ne pas commit) :

```env
# Base de données
DB_NAME=learnai
DB_USER=postgres
DB_PASSWORD=kidjamo@
DB_HOST=localhost
DB_PORT=5432

# Sécurité
JWT_SECRET_KEY=enspd-learnai-jwt-secret-2024-secure
SECRET_KEY=enspd-flask-secret-2024-secure

# API Chatbot (choisir l'une des deux)
GROQ_API_KEY=gsk_votre_cle_groq_ici
# GEMINI_API_KEY=AIzaSy_votre_cle_gemini_ici

# Configuration
DEBUG=True
```

---

## ⚠️ Sécurité

**Important :**
- Ne jamais commiter le fichier `.env` sur Git
- Utiliser des clés différentes pour dev et production
- Changer les clés par défaut en production
- Mettre `DEBUG=False` en production
- Utiliser des mots de passe forts pour la base de données

**Le fichier `.env` est déjà dans `.gitignore` ✅**

---

## 🧪 Vérification de la configuration

Pour vérifier que toutes les variables sont bien configurées :

```python
# backend/scripts/check_config.py
import os
from config import Config

required_vars = [
    'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT',
    'JWT_SECRET_KEY', 'SECRET_KEY'
]

print("Vérification de la configuration...")
for var in required_vars:
    value = getattr(Config, var, None)
    if value and value != "your_password_here" and value != "change-this-secret-key-in-production":
        print(f"✅ {var}: Configuré")
    else:
        print(f"❌ {var}: Non configuré ou valeur par défaut")

# Vérifier au moins une clé API chatbot
if Config.GROQ_API_KEY or Config.GEMINI_API_KEY:
    print("✅ Clé API chatbot: Configurée")
else:
    print("❌ Clé API chatbot: Non configurée")
```

---

## 📞 Support

Si vous avez des questions sur la configuration, consultez :
- `README.md` - Guide d'installation
- `DEPLOYMENT.md` - Guide de déploiement
- `.env.example` - Exemple de configuration

Ou ouvrez une issue sur GitHub.
