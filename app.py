"""Point d'entrée pour Azure App Service"""
import sys
import os

# Ajouter le répertoire backend au Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(current_dir, 'backend')
sys.path.insert(0, backend_path)

# Changer le répertoire de travail vers backend
os.chdir(backend_path)

# Importer l'application
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
