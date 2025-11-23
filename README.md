# 🎓 ENSPD LearnAI

Une plateforme intelligente d'assistance à l'apprentissage développée pour l'École Nationale Supérieure Polytechnique de Douala (ENSPD). Ce système combine l'intelligence artificielle et l'analyse de données pour offrir un suivi personnalisé des étudiants.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Vue d'ensemble

LearnAI est une solution complète qui aide les enseignants à suivre les performances de leurs étudiants et permet aux étudiants de bénéficier de recommandations personnalisées basées sur leurs résultats académiques. Le système utilise l'IA pour prédire les risques d'échec et suggérer des ressources pédagogiques adaptées.

### Fonctionnalités principales

**Pour les étudiants :**
- Consultation des notes et statistiques personnelles
- Recommandations de ressources pédagogiques adaptées au niveau
- Prédictions IA sur les performances futures
- Assistant chatbot intelligent pour répondre aux questions
- Visualisation des progrès par matière

**Pour les enseignants :**
- Tableau de bord avec statistiques de classe
- Gestion des notes et évaluations
- Identification automatique des étudiants en difficulté
- Filtres et pagination pour gérer de grandes classes
- Vue détaillée des performances par étudiant

**Système intelligent :**
- Analyse prédictive des performances
- Recommandations personnalisées de ressources
- Chatbot conversationnel (Groq/Gemini)
- Calcul automatique des moyennes et statistiques

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- PostgreSQL 13 ou supérieur
- Node.js (pour servir le frontend en développement)
- Un compte Groq ou Google Gemini pour le chatbot

### Configuration de la base de données

1. Installez PostgreSQL et créez une base de données :

```sql
CREATE DATABASE learnai;
```

2. Exécutez le script de création des tables :

```bash
psql -U postgres -d learnai -f database/schema.sql
```

3. Initialisez les données de test :

```bash
cd backend
python scripts/init_db.py
```

### Installation du backend

1. Créez un environnement virtuel Python :

```bash
python -m venv .venv
```

2. Activez l'environnement :

**Windows :**
```bash
.venv\Scripts\activate
```

**Linux/Mac :**
```bash
source .venv/bin/activate
```

3. Installez les dépendances :

```bash
cd backend
pip install -r requirements.txt
```

4. Créez un fichier `.env` à la racine du projet (copiez `.env.example`) :

```bash
cp .env.example .env
```

5. Configurez vos variables d'environnement dans `.env` :

```env
DB_PASSWORD=votre_mot_de_passe_postgres
GROQ_API_KEY=votre_clé_groq  # ou GEMINI_API_KEY
JWT_SECRET_KEY=votre_clé_secrète_jwt
SECRET_KEY=votre_clé_secrète_flask
```

6. Lancez le serveur :

```bash
python app.py
```

Le backend sera accessible sur `http://localhost:5000`

### Lancement du frontend

Ouvrez simplement `frontend/index.html` dans votre navigateur ou utilisez un serveur local :

```bash
# Avec Python
cd frontend
python -m http.server 8000

# Avec Node.js
npx http-server frontend -p 8000
```

Le frontend sera accessible sur `http://localhost:8000`

## 🔑 Comptes de démonstration

Après l'initialisation de la base de données, vous pouvez vous connecter avec :

**Enseignant :**
- Email : `enseignant@enspd.cm`
- Mot de passe : `teacher123`

**Étudiants :**
- Email : `etudiant1@enspd.cm` / Mot de passe : `student123` (Bon étudiant)
- Email : `etudiant2@enspd.cm` / Mot de passe : `student123` (Étudiant moyen)
- Email : `etudiant3@enspd.cm` / Mot de passe : `student123` (Étudiant en difficulté)

## 📁 Structure du projet

```
learnAI/
├── backend/
│   ├── app.py                 # Point d'entrée de l'application Flask
│   ├── config.py              # Configuration (BDD, API keys)
│   ├── models/                # Modèles de données
│   │   ├── database.py
│   │   └── user.py
│   ├── routes/                # Routes API
│   │   ├── auth_routes.py
│   │   ├── student_routes.py
│   │   ├── teacher_routes.py
│   │   ├── chatbot_routes.py
│   │   ├── grades_routes.py
│   │   └── settings.py
│   ├── services/              # Services métier
│   │   ├── auth_service.py
│   │   └── gemini_service.py
│   ├── ml/                    # Modèles d'IA
│   │   └── prediction_model.py
│   └── scripts/               # Scripts utilitaires
│       ├── init_db.py
│       └── add_resources.py
├── frontend/
│   ├── index.html             # Page de connexion
│   ├── dashboard-student.html # Tableau de bord étudiant
│   ├── dashboard-teacher.html # Tableau de bord enseignant
│   ├── grades.html            # Gestion des notes
│   ├── recommendations.html   # Recommandations
│   ├── chatbot.html           # Assistant IA
│   ├── settings.html          # Paramètres utilisateur
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── auth.js
│       ├── api.js
│       └── settings.js
├── database/
│   └── schema.sql             # Schéma de la base de données
└── docs/                      # Documentation
```

## 🛠️ Technologies utilisées

**Backend :**
- Flask (Framework web Python)
- PostgreSQL (Base de données)
- Flask-JWT-Extended (Authentification)
- Flask-CORS (Gestion CORS)
- bcrypt (Hachage des mots de passe)
- Groq/Gemini API (Chatbot IA)

**Frontend :**
- HTML5, CSS3, JavaScript vanilla
- Design responsive
- Fetch API pour les requêtes

**IA & Machine Learning :**
- Analyse prédictive des performances
- Système de recommandation basé sur les notes
- Chatbot conversationnel avec contexte

## 📊 Fonctionnalités détaillées

### Système de prédiction

Le système analyse les notes des étudiants pour :
- Calculer la probabilité de réussite
- Identifier les matières à risque
- Suggérer des actions correctives
- Prédire les notes futures

### Recommandations intelligentes

Les ressources sont recommandées selon :
- Le niveau de l'étudiant (débutant, intermédiaire, avancé)
- Les matières où il a des difficultés
- Son historique de consultation
- Les ressources qui ont aidé d'autres étudiants similaires

### Chatbot conversationnel

L'assistant IA peut :
- Répondre aux questions sur les cours
- Expliquer des concepts difficiles
- Donner des conseils d'étude
- Garder le contexte de la conversation

## 🔒 Sécurité

- Mots de passe hachés avec bcrypt
- Authentification JWT avec tokens
- Protection CORS configurée
- Validation des données côté serveur
- Sessions sécurisées

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Auteurs

Développé avec passion pour l'ENSPD - École Nationale Supérieure Polytechnique de Douala

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.

---

⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile !
