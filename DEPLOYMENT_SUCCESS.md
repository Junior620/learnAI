# 🎉 Déploiement Réussi - ENSPD LearnAI

## ✅ Application Déployée

**URL de Production:** https://learnai-2dnf.onrender.com

**Status:** ✅ En ligne et fonctionnelle

---

## 📝 Configuration Frontend

### Fichier créé: `frontend/js/config.js`

Ce fichier gère automatiquement l'URL de l'API selon l'environnement:
- **En local** (localhost): utilise `http://localhost:5000/api`
- **En production**: utilise `https://learnai-2dnf.onrender.com/api`

### ⚠️ Action Requise: Ajouter config.js dans les fichiers HTML

Dans **CHAQUE** fichier HTML du dossier `frontend/`, ajoute cette ligne **AVANT** les autres scripts:

```html
<script src="js/config.js"></script>
```

**Fichiers à modifier:**
1. `frontend/index.html`
2. `frontend/signup.html`
3. `frontend/dashboard-student.html`
4. `frontend/dashboard-teacher.html`
5. `frontend/grades.html`
6. `frontend/add-grade.html`
7. `frontend/chatbot.html`
8. `frontend/recommendations.html`
9. `frontend/settings.html`

**Exemple de placement:**
```html
<body>
    <!-- Contenu HTML -->
    
    <!-- Scripts - config.js DOIT être en premier -->
    <script src="js/config.js"></script>
    <script src="js/auth.js"></script>
    <script src="js/autres-scripts.js"></script>
</body>
```

---

## 🔐 Variables d'Environnement à Configurer sur Render

### Sur Render.com → Settings → Environment:

1. **SECRET_KEY** (déjà généré automatiquement ✅)
2. **JWT_SECRET_KEY** (déjà généré automatiquement ✅)

### Optionnel - Pour activer le chatbot:

3. **GROQ_API_KEY**
   - Va sur https://console.groq.com
   - Crée une clé API
   - Ajoute-la dans Render

### Optionnel - Pour la base de données PostgreSQL:

Si tu veux une vraie base de données (recommandé pour la production):

4. Sur Render, crée une **PostgreSQL Database** (gratuit)
5. Render te donnera automatiquement:
   - `DB_HOST`
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_PORT`
6. Copie ces valeurs dans les Environment Variables de ton service web

---

## 🚀 Prochaines Étapes

### 1. Tester l'API
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

### 2. Mettre à jour le Frontend
- Ajoute `<script src="js/config.js"></script>` dans tous les HTML
- Commit et push les changements
- Ouvre ton frontend et teste la connexion

### 3. Déployer le Frontend
Tu peux déployer le frontend sur:
- **Netlify** (recommandé, gratuit)
- **Vercel** (gratuit)
- **GitHub Pages** (gratuit)

---

## 📊 Informations Techniques

- **Plateforme:** Render.com
- **Plan:** Free (avec limitations)
- **Python:** 3.11.0
- **Serveur:** Gunicorn
- **Workers:** 1
- **Timeout:** 600s

### ⚠️ Limitation du Plan Gratuit
- L'app se met en veille après 15 min d'inactivité
- Premier accès après veille: ~30 secondes de démarrage
- Pour éviter ça: upgrade vers un plan payant ($7/mois)

---

## 🎯 Résumé des Fichiers Modifiés

### Créés:
- `wsgi.py` - Point d'entrée pour Render
- `frontend/js/config.js` - Configuration API
- `.python-version` - Force Python 3.11
- `requirements-light.txt` - Dépendances allégées
- `render.yaml` - Configuration Render

### Modifiés:
- `frontend/js/auth.js` - Utilise API_URL dynamique
- `frontend/js/settings.js` - Utilise API_URL dynamique
- `frontend/dashboard-teacher.html` - Utilise API_URL dynamique
- `backend/app.py` - Instance app au niveau module

---

## 🆘 Support

Si tu rencontres des problèmes:
1. Vérifie les logs sur Render Dashboard
2. Teste l'API directement avec curl
3. Vérifie que config.js est bien chargé dans le frontend (F12 → Console)

**Félicitations pour ton déploiement! 🎉**
