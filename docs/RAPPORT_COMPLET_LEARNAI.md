# RAPPORT DE PROJET GLO5

---

## ÉCOLE NATIONALE SUPÉRIEURE POLYTECHNIQUE DE DOUALA (ENSPD)

### Département de Génie Logiciel

---

# LEARNAI
## Plateforme Intelligente d'Assistance à l'Apprentissage

---

**Projet réalisé par :**

- DJOUNDA NGAPGHO MOMO CHRISTIAN
- EKOMO NTONGA YVAN LOIC  
- KEDDI NGALE

**Encadré par :**

Dr Maka Maka Ebenezer

**Année Académique :** 2025-2026

**Niveau :** 5ème année Génie Logiciel

---



## RÉSUMÉ

Le présent rapport décrit la conception et le développement de LearnAI, une plateforme web intelligente d'assistance à l'apprentissage destinée aux étudiants et enseignants de l'École Nationale Supérieure Polytechnique de Douala. Face aux défis croissants de la massification de l'enseignement supérieur et à la nécessité d'un suivi personnalisé des étudiants, nous avons développé un système qui exploite les technologies d'intelligence artificielle pour améliorer l'accompagnement pédagogique.

LearnAI intègre plusieurs modules fonctionnels : un système de gestion des notes, un moteur de recommandations personnalisées, un module de prédiction des performances académiques, et un assistant conversationnel intelligent. L'architecture repose sur une application web moderne avec un backend développé en Python (Flask) et un frontend en HTML/CSS/JavaScript, le tout connecté à une base de données PostgreSQL.

Le système utilise des algorithmes d'apprentissage automatique pour analyser les données académiques des étudiants et générer des prédictions sur leurs performances futures. Il identifie automatiquement les étudiants en difficulté et propose des ressources pédagogiques adaptées à leur niveau et à leurs besoins spécifiques. L'assistant conversationnel, alimenté par l'API Groq, offre un accompagnement personnalisé en répondant aux questions des étudiants et en leur fournissant des conseils d'étude contextualisés.


---



## TABLE DES MATIÈRES

1. [INTRODUCTION GÉNÉRALE](#introduction-générale)
2. [CAHIER DE CHARGES](#cahier-de-charges)
3. [ANALYSE ET CONCEPTION](#analyse-et-conception)
4. [FONCTIONNEMENT GLOBAL DE L'APPLICATION](#fonctionnement-global)
5. [MANUEL D'UTILISATION](#manuel-dutilisation)
6. [TESTS ET VALIDATION](#tests-et-validation)
7. [CONCLUSION GÉNÉRALE](#conclusion-générale)
8. [BIBLIOGRAPHIE](#bibliographie)

---



## 1. INTRODUCTION GÉNÉRALE

### 1.1 Contexte académique

L'École Nationale Supérieure Polytechnique de Douala forme chaque année des centaines d'ingénieurs dans divers domaines technologiques. Avec l'augmentation constante des effectifs étudiants, les enseignants font face à des difficultés croissantes pour assurer un suivi personnalisé de chaque apprenant. Cette situation peut conduire à une détection tardive des difficultés académiques et, dans certains cas, à des échecs qui auraient pu être évités avec un accompagnement adapté.



### 1.2 Problématique

Comment exploiter les technologies d'intelligence artificielle pour améliorer le suivi pédagogique des étudiants et leur proposer un accompagnement personnalisé basé sur l'analyse de leurs performances académiques ?

Cette question soulève plusieurs enjeux :
- La nécessité de centraliser et d'analyser les données académiques de manière structurée
- L'identification précoce des étudiants en difficulté avant qu'il ne soit trop tard
- La personnalisation des recommandations pédagogiques en fonction du profil de chaque étudiant
- L'automatisation partielle du suivi pour libérer du temps aux enseignants
- La mise à disposition d'un assistant intelligent accessible à tout moment



### 1.3 Objectifs du projet

L'objectif principal de ce projet est de concevoir et développer une plateforme web intelligente qui facilite le suivi pédagogique et améliore l'accompagnement des étudiants grâce à l'intelligence artificielle.

Les objectifs spécifiques sont les suivants :

**Pour les étudiants :**
- Offrir une vue claire et synthétique de leurs performances académiques
- Fournir des prédictions sur leurs chances de réussite dans chaque matière
- Recommander automatiquement des ressources pédagogiques adaptées à leur niveau
- Mettre à disposition un assistant conversationnel capable de répondre à leurs questions

**Pour les enseignants :**
- Centraliser la gestion des notes dans une interface intuitive
- Identifier rapidement les étudiants nécessitant une attention particulière
- Visualiser les statistiques de performance de leurs classes
- Faciliter le suivi individuel grâce à des tableaux de bord détaillés

**Sur le plan technique :**
- Développer une architecture web moderne, scalable et maintenable
- Implémenter des algorithmes d'apprentissage automatique pour l'analyse prédictive
- Intégrer des services d'intelligence artificielle pour le chatbot
- Assurer la sécurité des données et la confidentialité des informations personnelles



---



## 2. CAHIER DE CHARGES DU PROJET LEARNAI

### 2.1 Présentation du besoin

L'ENSPD, comme de nombreux établissements d'enseignement supérieur, fait face à des défis importants en matière de suivi pédagogique. Les promotions comptent souvent plusieurs dizaines d'étudiants par classe, rendant difficile un accompagnement individualisé. Les enseignants disposent de peu d'outils pour identifier rapidement les étudiants en difficulté, et les étudiants eux-mêmes manquent de visibilité sur leur progression et les actions à entreprendre pour s'améliorer.

Le besoin identifié est donc double : d'une part, fournir aux enseignants des outils d'analyse et de suivi efficaces ; d'autre part, offrir aux étudiants un accompagnement personnalisé et accessible à tout moment. L'intelligence artificielle apparaît comme une solution prometteuse pour répondre à ces besoins en automatisant certaines tâches d'analyse et en fournissant des recommandations pertinentes basées sur les données.

### 2.2 Objectifs fonctionnels

#### 2.2.1 Gestion des utilisateurs et authentification
- Permettre l'inscription et la connexion sécurisée des utilisateurs (étudiants, enseignants)
- Gérer différents niveaux d'accès selon le rôle (étudiant, enseignant, administrateur)
- Assurer la confidentialité des données personnelles et académiques
- Permettre la modification des informations de profil

#### 2.2.2 Gestion des notes et évaluations
- Permettre aux enseignants de saisir et modifier les notes des étudiants
- Organiser les notes par matière, type d'évaluation et semestre
- Calculer automatiquement les moyennes par matière et la moyenne générale
- Afficher l'historique complet des notes pour chaque étudiant

#### 2.2.3 Tableau de bord étudiant
- Afficher une vue synthétique des performances académiques
- Présenter les statistiques clés (moyenne générale, nombre de matières, progression)
- Visualiser les notes par matière sous forme de graphiques
- Afficher les prédictions de réussite et le niveau de risque

#### 2.2.4 Tableau de bord enseignant
- Afficher les statistiques globales de la classe (moyenne, taux de réussite)
- Lister tous les étudiants avec leurs performances
- Identifier visuellement les étudiants en difficulté
- Permettre le filtrage et la recherche d'étudiants
- Accéder aux détails de performance de chaque étudiant

#### 2.2.5 Système de recommandations
- Analyser les performances de l'étudiant pour identifier ses points faibles
- Recommander des ressources pédagogiques adaptées (PDF, vidéos, exercices)
- Personnaliser les recommandations selon le niveau de difficulté
- Permettre le suivi des ressources consultées

#### 2.2.6 Prédictions académiques
- Calculer la probabilité de réussite de l'étudiant
- Identifier les matières à risque
- Évaluer le niveau de risque global (faible, moyen, élevé)
- Fournir des explications sur les facteurs influençant les prédictions

#### 2.2.7 Assistant conversationnel (Chatbot)
- Répondre aux questions des étudiants sur leurs notes et performances
- Fournir des conseils d'étude personnalisés
- Expliquer des concepts académiques
- Maintenir le contexte de la conversation
- Accéder aux données réelles de l'étudiant pour des réponses précises

### 2.3 Objectifs non fonctionnels

#### 2.3.1 Performance
- Temps de réponse inférieur à 2 secondes pour les requêtes standards
- Temps de réponse du chatbot inférieur à 5 secondes
- Capacité à gérer au moins 100 utilisateurs simultanés
- Optimisation des requêtes base de données avec indexation

#### 2.3.2 Sécurité
- Chiffrement des mots de passe avec bcrypt
- Authentification par tokens JWT avec expiration
- Protection contre les injections SQL
- Configuration CORS sécurisée
- Validation des données côté serveur

#### 2.3.3 Utilisabilité
- Interface intuitive ne nécessitant pas de formation
- Design responsive fonctionnant sur mobile, tablette et desktop
- Messages d'erreur clairs et informatifs
- Navigation fluide entre les différentes sections

#### 2.3.4 Maintenabilité
- Code structuré et commenté
- Architecture modulaire facilitant les évolutions
- Documentation technique complète
- Utilisation de conventions de nommage cohérentes




## 3. ANALYSE ET CONCEPTION

### 3.1 Architecture générale du système

LearnAI repose sur une architecture client-serveur classique à trois tiers, séparant clairement la présentation, la logique métier et les données. Cette architecture offre plusieurs avantages : modularité, maintenabilité, et possibilité de faire évoluer chaque couche indépendamment.

**Couche présentation (Frontend)**
Notre frontend est une application web monopage développée en HTML5, CSS3 et JavaScript vanilla. Nous avons fait le choix de ne pas utiliser de framework JavaScript lourd (React, Vue, Angular) pour plusieurs raisons : simplicité de déploiement, performance, et maîtrise complète du code. L'interface est responsive et s'adapte automatiquement aux différentes tailles d'écran.

**Couche logique (Backend)**
Le backend est développé en Python avec le framework Flask. Il expose une API REST qui gère toutes les opérations métier : authentification, gestion des notes, calcul des statistiques, génération de recommandations, et interaction avec le chatbot. Flask a été choisi pour sa légèreté, sa flexibilité et sa large communauté.

**Couche données (Base de données)**
PostgreSQL a été retenu comme système de gestion de base de données pour sa robustesse, ses performances et sa conformité aux standards SQL. La base contient toutes les données de l'application : utilisateurs, notes, ressources, recommandations, conversations du chatbot, etc.

*Insérer schéma d'architecture ici*

### 3.2 Architecture détaillée

#### 3.2.1 Architecture backend

Le backend suit une architecture en couches respectant le principe de séparation des responsabilités :

**Couche routes (Controllers)**
Les routes définissent les points d'entrée de l'API. Chaque module fonctionnel possède son propre blueprint Flask :
- `auth_routes.py` : Authentification et gestion des sessions
- `student_routes.py` : Fonctionnalités pour les étudiants
- `teacher_routes.py` : Fonctionnalités pour les enseignants
- `chatbot_routes.py` : Interaction avec l'assistant conversationnel
- `grades_routes.py` : Gestion des notes
- `settings.py` : Paramètres utilisateurs

**Couche services (Business Logic)**
Les services contiennent la logique métier complexe :
- `auth_service.py` : Logique d'authentification et autorisation
- `groq_service.py` : Service de chatbot utilisant l'API Groq

**Couche modèles (Data Access)**
Les modèles encapsulent l'accès aux données :
- `database.py` : Gestion des connexions et requêtes PostgreSQL
- `user.py` : Modèle utilisateur avec méthodes d'authentification

**Couche ML (Machine Learning)**
Le module d'apprentissage automatique contient :
- `prediction_model.py` : Modèle de prédiction des performances
- `data_preprocessing.py` : Préparation des données pour l'entraînement

#### 3.2.2 Architecture frontend

Le frontend est organisé de manière modulaire :

**Pages HTML**
Chaque fonctionnalité majeure possède sa propre page :
- `index.html` : Page de connexion
- `dashboard-student.html` : Tableau de bord étudiant
- `dashboard-teacher.html` : Tableau de bord enseignant
- `grades.html` : Consultation des notes
- `recommendations.html` : Recommandations personnalisées
- `chatbot.html` : Interface du chatbot
- `settings.html` : Paramètres utilisateur

**Scripts JavaScript**
Les scripts sont organisés par responsabilité :
- `auth.js` : Gestion de l'authentification côté client
- `api.js` : Fonctions d'appel aux API backend
- `config.js` : Configuration (URL de l'API, constantes)

**Styles CSS**
Un fichier CSS unique (`style.css`) assure la cohérence visuelle de toute l'application.

### 3.3 Modèle de données

La base de données PostgreSQL est structurée autour de plusieurs tables interconnectées. Voici la description détaillée de chaque table :

#### 3.3.1 Table `users`
Stocke les informations de base de tous les utilisateurs du système.

| Colonne | Type | Description |
|---------|------|-------------|
| id | SERIAL PRIMARY KEY | Identifiant unique auto-incrémenté |
| email | VARCHAR(255) UNIQUE | Adresse email (identifiant de connexion) |
| password_hash | VARCHAR(255) | Mot de passe haché avec bcrypt |
| first_name | VARCHAR(100) | Prénom de l'utilisateur |
| last_name | VARCHAR(100) | Nom de famille |
| role | VARCHAR(20) | Rôle (student, teacher, admin) |
| created_at | TIMESTAMP | Date de création du compte |
| updated_at | TIMESTAMP | Date de dernière modification |

#### 3.3.2 Table `student_profiles`
Contient les informations spécifiques aux étudiants.

| Colonne | Type | Description |
|---------|------|-------------|
| id | SERIAL PRIMARY KEY | Identifiant unique |
| user_id | INTEGER | Référence vers users(id) |
| student_id | VARCHAR(50) UNIQUE | Matricule étudiant |
| department | VARCHAR(100) | Département (ex: Génie Logiciel) |
| level | VARCHAR(50) | Niveau (ex: L3, M1) |
| academic_year | VARCHAR(20) | Année académique (ex: 2024-2025) |
| created_at | TIMESTAMP | Date de création du profil |

#### 3.3.3 Table `subjects`
Liste des matières enseignées.

| Colonne | Type | Description |
|---------|------|-------------|
| id | SERIAL PRIMARY KEY | Identifiant unique |
| name | VARCHAR(100) | Nom de la matière |
| code | VARCHAR(20) UNIQUE | Code de la matière |
| department | VARCHAR(100) | Département concerné |
| credits | INTEGER | Nombre de crédits |
| teacher_id | INTEGER | Référence vers l'enseignant |
| created_at | TIMESTAMP | Date de création |

#### 3.3.4 Table `grades`
Stocke toutes les notes des étudiants.

| Colonne | Type | Description |
|---------|------|-------------|
| id | SERIAL PRIMARY KEY | Identifiant unique |
| student_id | INTEGER | Référence vers users(id) |
| subject_id | INTEGER | Référence vers subjects(id) |
| grade_type | VARCHAR(50) | Type (CC, Examen, TP, etc.) |
| score | DECIMAL(5,2) | Note sur 20 |
| max_score | DECIMAL(5,2) | Note maximale (défaut 20) |
| semester | VARCHAR(20) | Semestre (S1, S2) |
| academic_year | VARCHAR(20) | Année académique |
| created_at | TIMESTAMP | Date de saisie |

#### 3.3.5 Table `resources`
Catalogue des ressources pédagogiques.

| Colonne | Type | Description |
|---------|------|-------------|
| id | SERIAL PRIMARY KEY | Identifiant unique |
| title | VARCHAR(255) | Titre de la ressource |
| description | TEXT | Description détaillée |
| resource_type | VARCHAR(50) | Type (pdf, video, exercise, article) |
| url | TEXT | URL de la ressource |
| file_path | TEXT | Chemin du fichier si hébergé localement |
| subject_id | INTEGER | Matière concernée |
| difficulty_level | VARCHAR(20) | Niveau (beginner, intermediate, advanced) |
| tags | TEXT[] | Mots-clés pour la recherche |
| created_by | INTEGER | Créateur de la ressource |
| created_at | TIMESTAMP | Date d'ajout |

#### 3.3.6 Table `recommendations`
Historique des recommandations faites aux étudiants.

| Colonne | Type | Description |
|---------|------|-------------|
| id | SERIAL PRIMARY KEY | Identifiant unique |
| student_id | INTEGER | Étudiant concerné |
| resource_id | INTEGER | Ressource recommandée |
| subject_id | INTEGER | Matière concernée |
| recommendation_score | DECIMAL(5,4) | Score de pertinence (0-1) |
| reason | TEXT | Explication de la recommandation |
| status | VARCHAR(20) | Statut (pending, viewed, completed, dismissed) |
| created_at | TIMESTAMP | Date de la recommandation |

#### 3.3.7 Table `predictions`
Prédictions générées par le système.

| Colonne | Type | Description |
|---------|------|-------------|
| id | SERIAL PRIMARY KEY | Identifiant unique |
| student_id | INTEGER | Étudiant concerné |
| subject_id | INTEGER | Matière (NULL si prédiction globale) |
| prediction_type | VARCHAR(50) | Type de prédiction |
| predicted_score | DECIMAL(5,2) | Note prédite |
| success_probability | DECIMAL(5,4) | Probabilité de réussite (0-1) |
| risk_level | VARCHAR(20) | Niveau de risque (low, medium, high) |
| factors | JSONB | Facteurs influençant la prédiction |
| created_at | TIMESTAMP | Date de la prédiction |

#### 3.3.8 Table `chatbot_conversations`
Historique des conversations avec le chatbot.

| Colonne | Type | Description |
|---------|------|-------------|
| id | SERIAL PRIMARY KEY | Identifiant unique |
| user_id | INTEGER | Utilisateur ayant posé la question |
| message | TEXT | Message de l'utilisateur |
| response | TEXT | Réponse du chatbot |
| context | JSONB | Contexte de la conversation |
| created_at | TIMESTAMP | Date de l'échange |

#### 3.3.9 Table `alerts`
Alertes générées par le système.

| Colonne | Type | Description |
|---------|------|-------------|
| id | SERIAL PRIMARY KEY | Identifiant unique |
| user_id | INTEGER | Utilisateur concerné |
| alert_type | VARCHAR(50) | Type d'alerte |
| title | VARCHAR(255) | Titre de l'alerte |
| message | TEXT | Contenu de l'alerte |
| severity | VARCHAR(20) | Gravité (info, warning, critical) |
| is_read | BOOLEAN | Statut de lecture |
| created_at | TIMESTAMP | Date de création |



### 3.4 Description des modules fonctionnels

#### 3.4.1 Module d'authentification

Ce module gère l'inscription, la connexion et la gestion des sessions utilisateurs. Il utilise JWT (JSON Web Tokens) pour maintenir l'état d'authentification côté client. Lors de la connexion, le serveur génère un token signé contenant l'identifiant de l'utilisateur et son rôle. Ce token est ensuite envoyé avec chaque requête pour authentifier l'utilisateur.

Les mots de passe sont hachés avec bcrypt avant d'être stockés en base de données, garantissant qu'ils ne peuvent pas être récupérés même en cas de compromission de la base.

#### 3.4.2 Module de gestion des notes

Ce module permet aux enseignants de saisir, modifier et consulter les notes des étudiants. Il calcule automatiquement les moyennes par matière et la moyenne générale. Les notes sont organisées par type d'évaluation (contrôle continu, examen, travaux pratiques) et par semestre.

Le système vérifie que les notes sont dans l'intervalle valide (0-20) et empêche la saisie de doublons (même étudiant, même matière, même type d'évaluation pour un semestre donné).

#### 3.4.3 Module de recommandations

Le système de recommandations analyse les performances de l'étudiant pour identifier ses points faibles. Il compare ensuite ces faiblesses avec le catalogue de ressources disponibles et sélectionne celles qui correspondent au niveau de difficulté approprié.

L'algorithme de recommandation prend en compte plusieurs facteurs :
- La moyenne de l'étudiant dans la matière concernée
- Le type de ressource (privilégier les vidéos pour les concepts complexes)
- Le niveau de difficulté de la ressource
- Les ressources déjà consultées (éviter les doublons)

#### 3.4.4 Module de prédictions

Le module de prédictions utilise les données historiques de l'étudiant pour estimer ses chances de réussite. En l'absence de modèle ML entraîné (contrainte de mémoire sur le serveur gratuit), le système utilise des règles basées sur les moyennes :
- Moyenne ≥ 14 : Probabilité de réussite 95%, risque faible
- Moyenne ≥ 12 : Probabilité 80%, risque faible
- Moyenne ≥ 10 : Probabilité 60%, risque moyen
- Moyenne ≥ 8 : Probabilité 35%, risque élevé
- Moyenne < 8 : Probabilité 15%, risque élevé

Lorsque les ressources le permettent, un modèle de Gradient Boosting peut être entraîné sur les données historiques pour des prédictions plus précises.



### 3.5 Description du moteur d'intelligence artificielle

#### 3.5.1 Modèle de prédiction des performances

Le modèle de prédiction est basé sur l'algorithme Gradient Boosting Classifier de scikit-learn. Cet algorithme construit séquentiellement plusieurs arbres de décision, chacun corrigeant les erreurs du précédent.

**Features utilisées :**
- Moyenne générale de l'étudiant
- Écart-type des notes (mesure de la régularité)
- Note minimale et maximale
- Nombre total de notes
- Moyennes par matière (jusqu'à 6 matières principales)

**Target :**
La variable cible est binaire : réussite (moyenne ≥ 10) ou échec (moyenne < 10).

**Entraînement :**
Le modèle est entraîné sur l'ensemble des données historiques disponibles. Si moins de 5 étudiants sont présents, aucune séparation train/test n'est effectuée pour maximiser les données d'entraînement.

#### 3.5.2 Système de recommandations

Le système de recommandations utilise une approche basée sur le contenu (content-based filtering). Pour chaque étudiant, l'algorithme :

1. Identifie les matières où la moyenne est inférieure à 12/20
2. Récupère les ressources associées à ces matières
3. Filtre selon le niveau de difficulté approprié :
   - Moyenne < 8 : ressources niveau débutant
   - Moyenne 8-12 : ressources niveau intermédiaire
   - Moyenne > 12 : ressources niveau avancé
4. Calcule un score de pertinence basé sur l'écart entre la moyenne et le seuil de réussite
5. Trie les ressources par score décroissant


---



## 4. FONCTIONNEMENT GLOBAL DE L'APPLICATION

### 4.1 Parcours utilisateur général

L'utilisation de LearnAI commence par une phase d'authentification. L'utilisateur accède à la page de connexion où il saisit son adresse email et son mot de passe. Le système vérifie les identifiants et, en cas de succès, génère un token JWT qui sera utilisé pour toutes les requêtes ultérieures.

Une fois authentifié, l'utilisateur est redirigé vers son tableau de bord personnalisé selon son rôle. Les étudiants accèdent à une interface centrée sur leurs performances individuelles, tandis que les enseignants disposent d'outils de suivi de classe et de gestion des notes.

La navigation entre les différentes sections se fait via un menu latéral ou supérieur selon la taille de l'écran. Chaque page charge dynamiquement ses données depuis le backend via des appels API REST. Les données sont présentées sous forme de tableaux, graphiques et cartes statistiques pour faciliter leur compréhension.

### 4.2 Rôle et fonctionnalités pour les étudiants

#### 4.2.1 Consultation du tableau de bord

Le tableau de bord étudiant constitue le point d'entrée principal après la connexion. Il présente une vue synthétique des performances académiques avec plusieurs sections :

**Section statistiques clés**
En haut de page, trois cartes affichent les indicateurs principaux :
- La moyenne générale sur 20
- Le nombre total de matières suivies
- Le nombre total de notes enregistrées



#### 4.2.5 Gestion du profil

La page "Paramètres" permet à l'étudiant de :
- Consulter et modifier ses informations personnelles (nom, prénom, email)
- Mettre à jour son profil étudiant (matricule, département, niveau)
- Changer son mot de passe
- Configurer ses préférences (notifications, langue, thème)



### 4.3 Rôle et fonctionnalités pour les enseignants

#### 4.3.1 Vue d'ensemble de la classe

Le tableau de bord enseignant offre une vision globale des performances de la classe. Il présente :

**Statistiques de classe**
- Moyenne générale de la classe
- Nombre total d'étudiants
- Taux de réussite (pourcentage d'étudiants avec moyenne ≥ 10)
- Nombre d'étudiants en difficulté (moyenne < 10)

**Liste des étudiants**
Un tableau affiche tous les étudiants avec leurs performances :
- Nom et prénom
- Matricule
- Moyenne générale
- Nombre de notes
- Indicateur visuel du niveau de risque (pastille colorée)

Les étudiants en difficulté sont mis en évidence visuellement (fond rouge ou orange) pour attirer l'attention de l'enseignant.


#### 4.3.2 Gestion des notes

La page "Ajouter une note" permet à l'enseignant de saisir les évaluations. Le formulaire comprend :
- Sélection de l'étudiant (liste déroulante ou recherche)
- Sélection de la matière
- Type d'évaluation (CC, Examen, TP, Projet)
- Note sur 20
- Semestre
 académique


L'enseignant peut également modifier ou supprimer des notes existantes si nécessaire.

#### 4.3.3 Suivi individuel des étudiants

En cliquant sur un étudiant dans la liste, l'enseignant accède à une vue détaillée comprenant :
- Informations personnelles de l'étudiant
- Historique complet des notes
- Graphiques d'évolution des performances
- Prédictions de réussite
- Recommandations générées pour cet étudiant

Cette vue permet un suivi personnalisé et facilite les entretiens individuels avec les étudiants en difficulté.



#### 4.4 Traitement et analyse

Le système effectue plusieurs types de traitements sur ces données :

**Calculs statistiques**
- Moyennes par matière (moyenne arithmétique simple)
- Moyenne générale (moyenne de toutes les notes)
- Écart-type (mesure de la régularité des performances)
- Notes minimale et maximale

**Agrégations**
- Statistiques de classe (moyenne, médiane, taux de réussite)
- Comparaisons entre étudiants
- Évolutions temporelles

**Détection d'anomalies**
- Identification des chutes brutales de performance
- Détection des étudiants en décrochage
- Repérage des matières problématiques

#### 4.5.3 Génération de prédictions

Le processus de génération de prédictions suit ces étapes :

1. **Extraction des features**
   - Récupération de toutes les notes de l'étudiant
   - Calcul des statistiques (moyenne, écart-type, min, max)
   - Extraction des moyennes par matière

2. **Préparation des données**
   - Normalisation des features avec StandardScaler
   - Gestion des valeurs manquantes (remplacement par 0)
   - Construction du vecteur de features

3. **Prédiction**
   - Si le modèle ML est disponible : utilisation du Gradient Boosting
   - Sinon : application de règles basées sur les moyennes
   - Calcul de la probabilité de réussite
   - Détermination du niveau de risque

4. **Interprétation**
   - Identification des facteurs influençant la prédiction
   - Génération d'explications textuelles
   - Formulation de recommandations d'actions

### 4.6 Flux de données et interactions

#### 4.6.1 Flux d'authentification

1. L'utilisateur saisit email et mot de passe
2. Le frontend envoie une requête POST à `/api/auth/login`
3. Le backend vérifie les identifiants dans la base de données
4. Si valides, génération d'un token JWT contenant user_id et role
5. Le token est renvoyé au frontend et stocké dans localStorage
6. Toutes les requêtes ultérieures incluent ce token dans l'en-tête Authorization

#### 4.6.2 Flux de consultation des notes

1. L'étudiant accède à la page "Notes"
2. Le frontend envoie une requête GET à `/api/v2/student/dashboard` avec le token
3. Le backend extrait l'user_id du token
4. Requête SQL pour récupérer toutes les notes de cet étudiant
5. Calcul des moyennes et statistiques
6. Renvoi des données au format JSON
7. Le frontend affiche les données dans des tableaux et graphiques


---



## 5. MANUEL D'UTILISATION


### 5.2 Première connexion

#### 5.2.1 Page de connexion

Accédez à l'application via votre navigateur. Vouez sur la page de connexion.

*Capture d'écran : Page de connexion*

La page présente :
- Un formulaire avec champs email et mot de passe
- Un bouton "Se connecter"
- Un lien "Mot de passe oublié ?" (fonctionnalité future)

#### 5.2.2 Comptes de démonstration

Utilisez l'un des comptes suivants pour vous connecter :

**Compte enseignant :**
- Email : `enseignant@enspd.cm`
- Mot de passe : `teacher123`

**Comptes étudiants :**
- Email : `etudiant1@enspd.cm` / Mot de passe : `student123` (Bon étudiant, moyenne 15.48)
- Email : `etudiant2@enspd.cm` / Mot de passe : `student123` (Étudiant moyen, moyenne 11.25)
- Email : `etudiant3@enspd.cm` / Mot de passe : `student123` (Étudiant en difficulté, moyenne 8.75)

#### 5.2.3 Processus d'authentification

1. Saisissez votre email et mot de passe
2. Cliquez sur "Se connecter"
3. Si les identifiants sont corrects, vous êtes redirigé vers votre tableau de bord
4. Si incorrects, un message d'erreur s'affiche

### 5.3 Guide d'utilisation pour les étudiants

#### 5.3.1 Navigation dans le tableau de bord

Après connexion, vous arrivez sur votre tableau de bord personnel.

*Capture d'écran : Tableau de bord étudiant*

**Menu de navigation**

Le menu latéral (ou supérieur sur mobile) contient les liens suivants :
- Tableau de bord : Vue d'ensemble de vos performances
- Notes : Détail de toutes vos évaluations
- Recommandations ources pédagogiques suggérées
- Assistant IA : Chatbot pour vos questions
- Paramètres : Gestion de votre profil
- Déconnexion : Quitter l'application

**Section statistiques**

Trois cartes en haut de page affichent :
- Votre moyenne générale (ex: 15.48/20)
- Le nombre de matières suivies (ex: 6 matières)
- Le nombre total de notes (ex: 24 notes)

**Section prédictions**

Une carte dédiée présente :
- Votre probabilité de réussite (ex: 95%)
- Votre niveau de risque (Faible, Moyen, Élevé)
- Un message persnalisé selon votre situation

**Tableau des performances par matière**
n tableau liste toutes vos matières avec :
- Le nom de la matière
- Votre moyenne dans cette matière
- Le nombre de notes prises en compte
- Une barre de progression visuelle

#### 5.3.2 Consultation des notes

Cliquez sur "Notes" dans le menu pour accéder à la page détaillée.

*Capture d'écran : Page des notes*

Cette page affiche toutes vos évaluations sous forme de tableau :
- Matière
- Type d'évaluation (CC, Examen, TP)
- Note obtenue
- Semestre
- Date de saisie

**Utilisation des filtres**

Vous pouvez filtrer les notes par :
- Matière spécifique (menu déroulant)
- Semestre (S1, S2)
- Type d'évaluation

**Interprétation des résultats**

Les notes sont colorées selon leur r :
- Vert : Note ≥ 14 (très bien)
- Bleu : Note entre 12 et 14 (bien)
- Orange : Note entre 10 et 12 (passable)
- Rouge : Note < 10 (insuffisant)

#### 5.3.3 Consultation des recommandations

Cliquez sur "Recommandations" pour voir les ressources suggérées.

*Captd'écran : Page des recommandations*

Chaque recommandation présente :
- Le titre de la ressource
- description du contenu
- Le type (PDF, Vidéo, Exercice, Article)
- Le niveau de difficulté
- La matière concernée
- Un bouton "Accéder" pour ouvrir la ressource


###Utilisation du chatbot LearnBot

Cliquez sur "Assistant IA" pour accéder au chatbot.

*Capture d'ran : Interface du chatbot***Interface du chatbot**

L'interface ressemble à une application de messagerie :
- Zone de messages enichant l'historique
- Champ de saisie en bas
- Bouton "Envoyer" à droite

**Message de bienvenue**

LearnBot vous accueille avec un message présentant ses capacités :
- Explications de cours
- Conseils d'étude
- Analyse de vos performances
- Recommandations personnalisées


#### 5.3.5 Gestion de votre profil

Cliquez sur "Paramètres" pour accéder à vos informations personnelles.

*Capture d'écran : Page des paramètres*

**Onglet Profil**

Vous pouvez modifier :
- Votre prénom et nom
- Votre adresse email
- Votre matricule étudiant
- Votre département
- Votre niveau (L1, L2, L3, M1, M2)
- Votre année académique

Cliquez sur "Enregistrer les modifications" pour sauvegarder.

**Onglet Sécurité**

Pour changer votre mot de passe :
1. Saisissez votre mot de passe actuel
2. Entrez votre nouveau mot de passe (minimum 6 caractères)
3. Confirmez le nouveau mot de passe
4. Cliquez sur "Changer le mot de passe"

**Onglet Préférences**

Configurez vos préférences :
- Mode sombre (activer/désactiver)
- Langue de l'interface (Français/English)
- Notifications par email
- Alertes pour les nouvelles notes
- Alertes pour les recommandations

### 5.4 Guide d'utilisation pour les enseignants

#### 5.4.1 Vue d'ensemble de la classe

Après connexion, vous accédez au tableau de bord enseignant.

*Capture d'écran : Tableau de bord enseignant*

**Statistiques de classe**

Quatre cartes affichent les indicateurs clés :
- Moyenne générale de la classe
- Nombre total d'étudiants
- Taux de réussite (% d'étudiants avec moyenne ≥ 10)
- Nombre d'étudiants en difficulté

**Liste des étudiants**

Un tablente tous les étudiants avec :
- Nom et prénom
- Matricule
- Moyenne générale
- Nombre de notes
- Indicateur de risque (pastille colorée)

Les étudiants en difficulté sont mis en évidence avec un fond coloré (rouge ou orange).


#### 5.4.2 Ajout et gestion des notes

Cliquez sur "Ajouter une note" dans le menu.

*Capture d'écran : Formulaire d'ajout de note*

**Remplir le formulaire**

1. **Sélectionner l'étudiant** : Utilisez la liste déroulante ou tapez pour rechercher
2. **Choisir la matière** : Sélectionnez dans la liste des matières disponibles
3. **Type d'évaluation** : CC (Contrôle Continu), Examen, TP, Projet
4. **Note** : Saisissez la note sur 20 (ex: 15.5)
5. **e** : S1 ou S2
6. **Année académique** : Ex: 2024-2025

**Validation*
Cliquez sur "Enregistrer la note". Le système vérifie :
- Que la note est entre 0 et 20
existe pas déjà une note identique (même étudiant, matière, type, semestre)



**Modification d'une note**

Pour modifier une note existante :
1. Accédez à la liste des notes
2. Cliquez sur l'icône "Modifier" à côté de la note
3. Modifiez les valeurs souhaitées
4. Enregistrez les modifications

**Suppression d'une note**

Pour supprimer une note :
1. Accédez à la liste des notes
2. Cliquez sur l'icône "Supprimer"
3. Confirmez la suppression

#### 5.4.3 Suivi individuel d'un étudiant

Dans la liste des étudiants, cliquez sur le nom d'un étudiant pour accéder à sa fiche détaillée.

*Ce d'écran : Fiche détaillée d'un étudiant*

**Informations générales**

En haut de page :
- Nom complet de l'étudiant
- Matricule
- Département et niveau
- Photo de profil (initiales si pas de photo)

**Statistiques de performance**

Cartes affichant :
- Moyenne générale
- Nombre de notes
- Pre réussite
- Niveau de risque

**Historique des notes**

Tableau complet de toutes les notes de l'étudtière
- Type d'évaluation
- Note
- Semestre
- Date


#### 5.5.2 Comprendre le niveau de risque

Le niveau de risque est une catégorisation simplifiée :sque faible (vert)**
- Moyenne ≥ 12/20
- Performances stables
- Aucune matière en échec critique
- Action : Maintenir les efforts, viser l'excellence

**Risque moyen (orange)**
- Moyenne entre 10 et 12/20
- Quelques difficultés dans certaines matières
- Performances irrégulières
- Action : Identifier les points faibles, utiliser les recommandations

**Risque élevé (rouge)**
- Moyenne < 10/20
- Plusieurs matières en échec
- Tendancla baissection : Accompagnement urgent, plan de remédiation



#### 6.5.3 Sécurité

Plusieurs mesures de sécurité ont été implémentées :
- Hachage des mots de passe avec bcrypt
- Authentification par tokens JWT
- Requêtes SQL paramétrées (protection contre injection)
- Validation des données côté serveur
- Configuration CORS appropriée
- Pas de données sensibles dans le code source

---