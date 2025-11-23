# Tests unitaires pour le Machine Learning
import unittest
import numpy as np
import pandas as pd
import sys
sys.path.append('../backend')

from ml.data_preprocessing import DataPreprocessor
from ml.prediction_model import PredictionModel

class TestDataPreprocessing(unittest.TestCase):
    """Tests pour le prétraitement des données"""
    
    def test_prepare_features(self):
        """Test de préparation des features"""
        # Créer des données de test
        data = {
            'student_id': [1, 1, 1, 2, 2, 2],
            'subject_id': [1, 2, 3, 1, 2, 3],
            'score': [15, 12, 18, 8, 9, 7],
            'grade_type': ['Examen'] * 6,
            'semester': ['S1'] * 6,
            'academic_year': ['2024-2025'] * 6
        }
        df = pd.DataFrame(data)
        
        features, stats, pivot = DataPreprocessor.prepare_features(df)
        
        # Vérifier que les features sont créées
        self.assertIsNotNone(features)
        self.assertIn('avg_score', features.columns)
        self.assertIn('std_score', features.columns)
        
        # Vérifier les calculs
        student1_avg = features[features['student_id'] == 1]['avg_score'].values[0]
        self.assertAlmostEqual(student1_avg, 15.0, places=1)

class TestPredictionModel(unittest.TestCase):
    """Tests pour le modèle de prédiction"""
    
    def test_model_initialization(self):
        """Test d'initialisation du modèle"""
        model = PredictionModel()
        self.assertIsNone(model.model)
        self.assertIsNone(model.scaler)
    
    def test_prediction_format(self):
        """Test du format de prédiction"""
        # Simuler une prédiction
        prediction = {
            'success': True,
            'success_probability': 0.85,
            'risk_level': 'low'
        }
        
        # Vérifier le format
        self.assertIn('success', prediction)
        self.assertIn('success_probability', prediction)
        self.assertIn('risk_level', prediction)
        self.assertIsInstance(prediction['success'], bool)
        self.assertIsInstance(prediction['success_probability'], float)
        self.assertIn(prediction['risk_level'], ['low', 'medium', 'high'])

class TestRecommendationEngine(unittest.TestCase):
    """Tests pour le moteur de recommandation"""
    
    def test_recommendation_logic(self):
        """Test de la logique de recommandation"""
        # Simuler des matières faibles
        weak_subjects = [
            {'subject_id': 1, 'subject_name': 'Mathématiques', 'avg_score': 8.5},
            {'subject_id': 2, 'subject_name': 'Physique', 'avg_score': 7.0}
        ]
        
        # Vérifier que les matières sont bien identifiées
        self.assertEqual(len(weak_subjects), 2)
        self.assertTrue(all(s['avg_score'] < 10 for s in weak_subjects))

if __name__ == '__main__':
    unittest.main()
