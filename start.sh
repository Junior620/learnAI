#!/bin/bash

echo "========================================"
echo "ENSPD LearnAI - Démarrage"
echo "========================================"
echo ""

# Vérifier PostgreSQL
echo "Vérification de PostgreSQL..."
if ! command -v psql &> /dev/null; then
    echo "[ERREUR] PostgreSQL n'est pas installé"
    exit 1
fi
echo "[OK] PostgreSQL est accessible"
echo ""

# Vérifier/créer la base de données
echo "Vérification de la base de données..."
if ! psql -U postgres -lqt | cut -d \| -f 1 | grep -qw learnai; then
    echo "Création de la base de données learnai..."
    psql -U postgres -c "CREATE DATABASE learnai;"
    echo "Importation du schéma..."
    psql -U postgres -d learnai -f database/schema.sql
    echo "[OK] Base de données créée"
else
    echo "[OK] Base de données existe"
fi
echo ""

# Installer les dépendances
echo "Installation des dépendances Python..."
cd backend
pip install -r requirements.txt > /dev/null 2>&1
echo "[OK] Dépendances installées"
echo ""

# Initialiser les données
echo "Initialisation des données de test..."
python scripts/init_db.py
echo ""

# Démarrer le backend
echo "Démarrage du backend..."
python app.py &
BACKEND_PID=$!
echo "[OK] Backend démarré sur http://localhost:5000 (PID: $BACKEND_PID)"
echo ""

# Démarrer le frontend
echo "Démarrage du frontend..."
cd ../frontend
python -m http.server 8000 &
FRONTEND_PID=$!
echo "[OK] Frontend démarré sur http://localhost:8000 (PID: $FRONTEND_PID)"
echo ""

echo "========================================"
echo "Application démarrée avec succès!"
echo ""
echo "Frontend: http://localhost:8000"
echo "Backend API: http://localhost:5000"
echo ""
echo "Comptes de test:"
echo "  Enseignant: enseignant@enspd.cm / teacher123"
echo "  Étudiant: etudiant1@enspd.cm / student123"
echo "========================================"
echo ""
echo "Pour arrêter l'application:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Ouvrir le navigateur
sleep 2
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8000
elif command -v open &> /dev/null; then
    open http://localhost:8000
fi

# Attendre
wait
