# Modèle de prédiction Machine Learning
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import sys

# Ajouter le répertoire parent au path si nécessaire
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from ml.data_preprocessing import DataPreprocessor
except ImportError:
    from data_preprocessing import DataPreprocessor

class PredictionModel:
    """Modèle ML pour prédire la réussite des étudiants"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.model_path = "ml/models/prediction_model.pkl"
        self.scaler_path = "ml/models/scaler.pkl"
    
    def train_model(self):
        """Entraîne le modèle de prédiction"""
        print("Récupération des données...")
        X, y, scaler = DataPreprocessor.create_training_data()
        
        if X is None or len(X) < 2:
            print("Pas assez de données pour l'entraînement (minimum 2 étudiants)")
            return False
        
        print(f"Données récupérées: {len(X)} étudiants")
        
        # Si peu de données, pas de séparation train/test
        if len(X) < 5:
            print("⚠️ Petit dataset détecté - Entraînement sans séparation train/test")
            X_train, y_train = X, y
            X_test, y_test = X, y  # Utiliser les mêmes données pour le test
        else:
            # Séparation train/test pour datasets plus grands
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
        
        print(f"Entraînement sur {len(X_train)} échantillons...")
        
        # Entraîner le modèle avec des paramètres adaptés aux petits datasets
        self.model = GradientBoostingClassifier(
            n_estimators=50,  # Réduit pour petits datasets
            learning_rate=0.1,
            max_depth=2,  # Réduit pour éviter l'overfitting
            random_state=42
        )
        self.model.fit(X_train, y_train)
        self.scaler = scaler
        
        # Évaluation
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\n✅ Précision du modèle: {accuracy:.2%}")
        
        if len(X) >= 5:
            print("\nRapport de classification:")
            print(classification_report(y_test, y_pred, zero_division=0))
        
        # Sauvegarder le modèle
        self.save_model()
        
        return True

    def save_model(self):
        """Sauvegarde le modèle entraîné"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        print(f"Modèle sauvegardé: {self.model_path}")
    
    def load_model(self):
        """Charge le modèle sauvegardé"""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
            return True
        return False
    
    def predict_success(self, student_id):
        """Prédit la probabilité de réussite d'un étudiant"""
        # Essayer de charger le modèle, mais continuer même s'il n'existe pas
        if self.model is None:
            self.load_model()  # Tenter de charger, mais ne pas échouer si absent
        
        # Préparer les données complètes de l'étudiant (avec moyennes par matière)
        from models.database import Database
        
        query = """
            SELECT 
                AVG(g.score) as avg_score,
                STDDEV(g.score) as std_score,
                MIN(g.score) as min_score,
                MAX(g.score) as max_score,
                COUNT(*) as num_grades
            FROM grades g
            WHERE g.student_id = %s
        """
        stats = Database.execute_query_one(query, (student_id,))
        
        if not stats or not stats['avg_score']:
            return None
        
        # Récupérer les moyennes par matière
        query_subjects = """
            SELECT subject_id, AVG(score) as avg_score
            FROM grades
            WHERE student_id = %s
            GROUP BY subject_id
            ORDER BY subject_id
            LIMIT 6
        """
        subject_avgs = Database.execute_query(query_subjects, (student_id,), fetch=True)
        
        # Créer le vecteur de features (5 stats + jusqu'à 6 moyennes par matière)
        features_list = [
            float(stats['avg_score']),
            float(stats['std_score']) if stats['std_score'] else 0.0,
            float(stats['min_score']),
            float(stats['max_score']),
            int(stats['num_grades'])
        ]
        
        # Ajouter les moyennes par matière (padding avec 0 si moins de 6)
        for i in range(6):
            if i < len(subject_avgs):
                features_list.append(float(subject_avgs[i]['avg_score']))
            else:
                features_list.append(0.0)
        
        # Variables par défaut pour prédiction basique
        prediction = 1  # Succès par défaut
        probability = None
        
        # Si le modèle n'est pas disponible, utiliser une prédiction basée sur la moyenne
        if self.model is None or self.scaler is None:
            print("⚠️ Modèle ML non disponible - Utilisation de prédiction basique")
        else:
            # Utiliser le modèle ML si disponible
            try:
                # Ajouter un feature supplémentaire si le modèle en attend 12
                if hasattr(self.model, 'n_features_in_') and self.model.n_features_in_ == 12:
                    features_list.append(0.0)  # department_encoded ou autre
                
                features = np.array([features_list])
                features_scaled = self.scaler.transform(features)
                prediction = self.model.predict(features_scaled)[0]
                probability = self.model.predict_proba(features_scaled)[0]
            except Exception as e:
                print(f"⚠️ Erreur ML: {e} - Utilisation de prédiction basique")
        
        # Calculer une probabilité basée sur la moyenne réelle
        avg = float(stats['avg_score'])
        
        # Calculer une probabilité plus réaliste basée sur la moyenne
        if avg >= 14:
            adjusted_prob = 0.95
            risk = 'low'
        elif avg >= 12:
            adjusted_prob = 0.80
            risk = 'low'
        elif avg >= 10:
            adjusted_prob = 0.60
            risk = 'medium'
        elif avg >= 8:
            adjusted_prob = 0.35
            risk = 'high'
        else:
            adjusted_prob = 0.15
            risk = 'high'
        
        return {
            'success': bool(prediction),
            'success_probability': adjusted_prob,
            'risk_level': risk
        }
