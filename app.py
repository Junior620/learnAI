"""Point d'entrée pour Azure App Service"""
import sys
import os

# Ajouter le répertoire backend au Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Importer l'application depuis backend
from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
