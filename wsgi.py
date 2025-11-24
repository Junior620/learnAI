import sys
import os

# Ajouter le backend au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Importer l'app
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
