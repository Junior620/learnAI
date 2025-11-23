# Script pour entraîner le modèle ML
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml.prediction_model import PredictionModel

def main():
    """Script principal pour entraîner le modèle"""
    print("=" * 50)
    print("ENSPD LearnAI - Entraînement du Modèle ML")
    print("=" * 50)
    
    model = PredictionModel()
    
    print("\n📊 Démarrage de l'entraînement...")
    success = model.train_model()
    
    if success:
        print("\n✅ Modèle entraîné et sauvegardé avec succès!")
        print(f"📁 Emplacement: {model.model_path}")
    else:
        print("\n❌ Échec de l'entraînement du modèle")
        print("Assurez-vous d'avoir des données dans la base de données")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
