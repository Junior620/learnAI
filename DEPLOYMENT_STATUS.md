# 📊 État du Déploiement - ENSPD LearnAI

## ✅ Ce qui fonctionne

### Backend (Render)
- ✅ **Déployé** sur https://learnai-2dnf.onrender.com
- ✅ **Base de données PostgreSQL** configurée et connectée
- ✅ **773,070 lignes de données** importées:
  - 10,007 utilisateurs
  - 10,006 profils étudiants
  - 752,784 notes
  - 6 matières
  - 146 ressources
  - 108 recommandations
  - 13 conversations chatbot

### Comptes de Test
- ✅ **Mots de passe réinitialisés** pour:
  - `etudiant1@enspd.cm` / `password123` (74 notes, moyenne 15.48/20)
  - `etudiant2@enspd.cm` / `password123`
  - `etudiant3@enspd.cm` / `password123`
  - `enseignant@enspd.cm` / `password123`

### API
- ✅ **Login fonctionnel**: `/api/auth/login`
- ✅ **Routes de debug**: `/api/admin/test-dashboard/5`
- ✅ **Routes v2 créées**: `/api/v2/student/*` (contournement bug JWT)

## ⚠️ Problème en cours

### Bug Flask-JWT-Extended + PyJWT
**Symptôme**: Erreur 422 "Subject must be a string"

**Cause**: Flask-JWT-Extended génère des tokens JWT avec `sub` (user_id) en integer, mais PyJWT 2.8.0 exige que `sub` soit une string selon la spec RFC 7519.

**Solutions tentées**:
1. ❌ Mise à jour Flask-JWT-Extended 4.6.0
2. ❌ Désactivation des validations JWT (`verify_aud`, `verify_iss`)
3. 🔄 **En cours**: Downgrade PyJWT à 2.4.0 (version sans validation stricte)

**Dernier commit**: `b387c00` - "Downgrade PyJWT to 2.4.0 to fix sub validation"

## 🎯 Prochaines étapes

### Option 1: Attendre le redéploiement Render
1. Vérifier que Render a déployé PyJWT 2.4.0
2. Tester avec:
```javascript
fetch('https://learnai-2dnf.onrender.com/api/auth/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({email: 'etudiant1@enspd.cm', password: 'password123'})
})
.then(r => r.json())
.then(d => {
    localStorage.setItem('token', d.access_token);
    localStorage.setItem('user', JSON.stringify(d.user));
    window.location.href = 'dashboard-student.html';
})
```

### Option 2: Déployer le Frontend (Recommandé)
Déployer le frontend sur **Netlify** ou **Vercel** pour:
- Éviter les problèmes de cache du navigateur
- Avoir une vraie URL de production
- Tester dans un environnement propre

**Commandes pour Netlify**:
```bash
# Installer Netlify CLI
npm install -g netlify-cli

# Déployer le frontend
cd frontend
netlify deploy --prod
```

### Option 3: Solution Alternative (Si PyJWT 2.4.0 ne marche pas)
Modifier Flask-JWT-Extended pour générer `sub` en string:

```python
# Dans routes/auth_routes.py
access_token = create_access_token(identity=str(user['id']))  # Convertir en string
```

## 📝 Notes Techniques

### Variables d'environnement Render
Toutes configurées:
- `DATABASE_URL`
- `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`
- `SECRET_KEY`, `JWT_SECRET_KEY`
- `GROQ_API_KEY` (pour le chatbot IA)
- `FLASK_ENV=production`
- `DEBUG=False`

### Frontend Configuration
- ✅ Pointe vers `https://learnai-2dnf.onrender.com/api`
- ✅ Utilise les routes v2 (`/api/v2/student/*`)

## 🐛 Logs de Debug

Pour voir les logs sur Render:
1. Dashboard Render → learnai-2dnf
2. Onglet "Logs"
3. Chercher: "Token invalide", "Erreur vérification token"

## 📞 Support

Si le problème persiste après le redéploiement avec PyJWT 2.4.0, contacter:
- Vérifier les logs Render
- Tester l'endpoint `/api/admin/test-token`
- Considérer le déploiement du frontend sur Netlify
