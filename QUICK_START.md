# 🚀 Quick Start - ENSPD LearnAI

## ✅ Ce qui est fait

1. ✅ **Backend déployé sur Render**
   - URL: https://learnai-2dnf.onrender.com
   - Status: En ligne et fonctionnel

2. ✅ **Frontend configuré**
   - Détection automatique de l'environnement (local/production)
   - Tous les fichiers HTML mis à jour avec `config.js`

3. ✅ **Code pushé sur GitHub**
   - Repo: https://github.com/Junior620/learnAI

---

## 🎯 Prochaines Étapes

### 1. Tester l'API (Maintenant)

Ouvre ton navigateur et va sur:
```
https://learnai-2dnf.onrender.com/
```

Tu devrais voir:
```json
{
  "message": "ENSPD LearnAI API",
  "version": "1.0.0",
  "status": "running"
}
```

### 2. Tester le Frontend en Local

```bash
# Ouvre simplement index.html dans ton navigateur
# L'API pointera automatiquement vers Render
```

### 3. Configurer les Variables d'Environnement (Optionnel)

Suis le guide: `RENDER_ENV_SETUP.md`

**Pour le chatbot:**
- Ajoute `GROQ_API_KEY` sur Render

**Pour la base de données:**
- Crée une PostgreSQL Database sur Render
- Lie-la à ton service web

### 4. Déployer le Frontend

**Option A: Netlify (Recommandé)**
1. Va sur https://app.netlify.com
2. Drag & drop le dossier `frontend/`
3. C'est tout!

**Option B: Vercel**
1. Va sur https://vercel.com
2. Import depuis GitHub
3. Root Directory: `frontend`
4. Deploy

**Option C: GitHub Pages**
1. Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: `/frontend`

---

## 📁 Structure du Projet

```
learnAI/
├── backend/              # API Flask
│   ├── app.py           # Application principale
│   ├── routes/          # Routes API
│   ├── models/          # Modèles de données
│   └── services/        # Services (ML, chatbot)
├── frontend/            # Interface utilisateur
│   ├── js/
│   │   ├── config.js    # ⭐ Configuration API
│   │   ├── auth.js      # Authentification
│   │   └── ...
│   └── *.html           # Pages
├── wsgi.py              # Point d'entrée Render
└── requirements.txt     # Dépendances Python
```

---

## 🔗 Liens Utiles

- **API Production:** https://learnai-2dnf.onrender.com
- **GitHub Repo:** https://github.com/Junior620/learnAI
- **Render Dashboard:** https://dashboard.render.com
- **Groq Console:** https://console.groq.com

---

## 📚 Documentation

- `DEPLOYMENT_SUCCESS.md` - Guide complet du déploiement
- `RENDER_ENV_SETUP.md` - Configuration des variables d'environnement
- `RENDER_DEPLOYMENT.md` - Instructions Render détaillées

---

## 🆘 Besoin d'Aide?

### L'API ne répond pas
```bash
# Vérifie le status
curl https://learnai-2dnf.onrender.com/

# Vérifie les logs sur Render Dashboard
```

### Le frontend ne se connecte pas
1. Ouvre la console du navigateur (F12)
2. Vérifie que `config.js` est chargé
3. Vérifie que `API_URL` pointe vers Render

### Erreur CORS
- Vérifie que `Flask-CORS` est bien configuré dans `backend/app.py`
- L'origine doit être autorisée

---

**Félicitations! Ton app est déployée et prête à l'emploi! 🎉**
