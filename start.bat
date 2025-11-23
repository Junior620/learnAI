<@echo off
echo ========================================
echo ENSPD LearnAI - Demarrage
echo ========================================
echo.

echo Verification de PostgreSQL...
psql -U postgres -c "SELECT version();" > nul 2>&1
if errorlevel 1 (
    echo [ERREUR] PostgreSQL n'est pas accessible
    echo Assurez-vous que PostgreSQL est installe et demarre
    pause
    exit /b 1
)
echo [OK] PostgreSQL est accessible
echo.

echo Verification de la base de donnees...
psql -U postgres -lqt | findstr /C:"learnai" > nul
if errorlevel 1 (
    echo Creation de la base de donnees learnai...
    psql -U postgres -c "CREATE DATABASE learnai;"
    echo Importation du schema...
    psql -U postgres -d learnai -f database\schema.sql
    echo [OK] Base de donnees creee
) else (
    echo [OK] Base de donnees existe
)
echo.

echo Installation des dependances Python...
cd backend
pip install -r requirements.txt > nul 2>&1
echo [OK] Dependances installees
echo.

echo Initialisation des donnees de test...
python scripts\init_db.py
echo.

echo Demarrage du backend...
start "ENSPD LearnAI Backend" python app.py
echo [OK] Backend demarre sur http://localhost:5000
echo.

echo Demarrage du frontend...
cd ..\frontend
start "ENSPD LearnAI Frontend" python -m http.server 8000
echo [OK] Frontend demarre sur http://localhost:8000
echo.

echo ========================================
echo Application demarree avec succes!
echo.
echo Frontend: http://localhost:8000
echo Backend API: http://localhost:5000
echo.
echo Comptes de test:
echo   Enseignant: enseignant@enspd.cm / teacher123
echo   Etudiant: etudiant1@enspd.cm / student123
echo ========================================
echo.
echo Appuyez sur une touche pour ouvrir le navigateur...
pause > nul
start http://localhost:8000
