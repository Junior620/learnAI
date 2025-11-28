"""
Script pour entraîner le modèle ML au démarrage
"""
import sys
import os

# Ajouter le répertoire backend au path
sys.path.insert(0, os.path.dirname(__file__))

from ml.prediction_model import PredictionModel

def train_model():
    """Entraîne le modèle de prédiction"""
    print("🤖 Entraînement du modèle ML...")
    
    try:
        model = PredictionModel()
        success = model.train_model()
        
        if success:
            print("✅ Modèle entraîné avec succès!")
            return True
        else:
            print("⚠️ Entraînement échoué - Le système utilisera des prédictions basiques")
            return False
    except Exception as e:
        print(f"❌ Erreur lors de l'entraînement: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    train_model()
