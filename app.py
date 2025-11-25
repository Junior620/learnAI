"""Point d'entrée pour Azure App Service"""
import sys
import os

# Ajouter le répertoire backend au Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(current_dir, 'backend')
sys.path.insert(0, backend_path)

# Importer create_app depuis le module app du backend
from app import create_app

# Créer l'instance de l'application Flask
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
