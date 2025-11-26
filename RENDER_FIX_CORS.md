# 🔧 Fix CORS et Variables d'Environnement sur Render

## Problème Actuel
- ❌ Erreur 500 sur `/api/auth/login`
- ❌ Variables d'environnement manquantes sur Render

## Solution: Configurer les Variables d'Environnement

### 1. Aller sur le Dashboard Render
1. Va sur https://dashboard.render.com
2. Clique sur ton service **learnai-2dnf**
3. Clique sur **Environment** dans le menu de gauche

### 2. Ajouter les Variables d'Environnement

Ajoute ces variables (clique sur **Add Environment Variable** pour chacune):

```
DATABASE_URL=postgresql://learnai_user:YgBxq88twjJwBVvQIOFYBjiWhwak9iUU@dpg-d4itr37diees73asg05g-a.frankfurt-postgres.render.com/learnai_kman

DB_HOST=dpg-d4itr37diees73asg05g-a.frankfurt-postgres.render.com

DB_NAME=learnai_kman

DB_USER=learnai_user

DB_PASSWORD=YgBxq88twjJwBVvQIOFYBjiWhwak9iUU

DB_PORT=5432

SECRET_KEY=votre-cle-secrete-super-longue-et-aleatoire-123456

JWT_SECRET_KEY=votre-jwt-secret-key-super-longue-et-aleatoire-789

GROQ_API_KEY=votre-cle-groq-api-ici

FLASK_ENV=production

DEBUG=False
```

### 3. Sauvegarder et Redéployer

1. Clique sur **Save Changes**
2. Render va automatiquement redéployer ton application
3. Attends 2-3 minutes que le déploiement se termine

### 4. Tester l'API

Une fois le déploiement terminé, teste avec:

```bash
curl https://learnai-2dnf.onrender.com/api/auth/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"student1@enspd.edu","password":"password123"}'
```

Tu devrais recevoir un token JWT!

### 5. Tester le Frontend

1. Rafraîchis ta page de login (Ctrl+F5)
2. Essaie de te connecter avec:
   - Email: `student1@enspd.edu`
   - Password: `password123`

## ✅ Résultat Attendu

Le frontend local devrait maintenant pouvoir communiquer avec le backend sur Render sans erreur CORS!

## 📝 Notes

- Le frontend a été configuré pour pointer vers `https://learnai-2dnf.onrender.com/api`
- Le CORS est déjà configuré dans `backend/app.py` pour accepter toutes les origines
- Une fois que tout fonctionne, tu pourras déployer le frontend sur Netlify/Vercel
