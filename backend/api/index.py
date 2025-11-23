# Point d'entrée pour Vercel Serverless
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app

app = create_app()

# Handler pour Vercel
def handler(request, context):
    return app(request.environ, context)
