# Prétraitement des données pour le Machine Learning
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import sys
import os

# Ajouter le répertoire parent au path si nécessaire
if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from models.database import Database
except ImportError:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from models.database import Database

class DataPreprocessor:
    """Classe pour le prétraitement des données académiques"""
    
    @staticmethod
    def fetch_student_grades():
        """Récupère toutes les notes des étudiants"""
        query = """
            SELECT 
                g.student_id,
                g.subject_id,
                s.name as subject_name,
                s.code as subject_code,
                g.score,
                g.grade_type,
                g.semester,
                g.academic_year,
                sp.department,
                sp.level
            FROM grades g
            JOIN subjects s ON g.subject_id = s.id
            JOIN users u ON g.student_id = u.id
            LEFT JOIN student_profiles sp ON u.id = sp.user_id
            ORDER BY g.student_id, g.created_at
        """
        results = Database.execute_query(query, fetch=True)
        return pd.DataFrame([dict(row) for row in results]) if results else pd.DataFrame()
    
    @staticmethod
    def prepare_features(df):
        """Prépare les features pour le ML"""
        if df.empty:
            return None, None, None
        
        # Calculer les statistiques par étudiant
        student_stats = df.groupby('student_id').agg({
            'score': ['mean', 'std', 'min', 'max', 'count']
        }).reset_index()
        
        student_stats.columns = ['student_id', 'avg_score', 'std_score', 'min_score', 'max_score', 'num_grades']
        
        # Calculer les moyennes par matière
        subject_stats = df.groupby(['student_id', 'subject_id']).agg({
            'score': 'mean'
        }).reset_index()
        
        subject_stats.columns = ['student_id', 'subject_id', 'subject_avg']
        
        # Pivoter pour avoir une colonne par matière
        subject_pivot = subject_stats.pivot(index='student_id', columns='subject_id', values='subject_avg')
        subject_pivot.columns = [f'subject_{col}_avg' for col in subject_pivot.columns]
        subject_pivot = subject_pivot.fillna(0)
        
        # Fusionner les statistiques
        features = student_stats.merge(subject_pivot, on='student_id', how='left')
        features = features.fillna(0)
        
        # Encoder les départements si disponibles
        if 'department' in df.columns:
            dept_encoder = LabelEncoder()
            df['department_encoded'] = dept_encoder.fit_transform(df['department'].fillna('Unknown'))
            dept_features = df.groupby('student_id')['department_encoded'].first().reset_index()
            features = features.merge(dept_features, on='student_id', how='left')
        
        return features, student_stats, subject_pivot
    
    @staticmethod
    def create_training_data():
        """Crée les données d'entraînement pour le modèle"""
        df = DataPreprocessor.fetch_student_grades()
        
        if df.empty:
            print("Aucune donnée disponible pour l'entraînement")
            return None, None, None
        
        features, _, _ = DataPreprocessor.prepare_features(df)
        
        if features is None:
            return None, None, None
        
        # Créer la variable cible (réussite/échec basé sur la moyenne)
        features['success'] = (features['avg_score'] >= 10).astype(int)
        
        # Séparer features et target
        X = features.drop(['student_id', 'success'], axis=1)
        y = features['success']
        
        # Normaliser les features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        return X_scaled, y, scaler
    
    @staticmethod
    def prepare_student_data_for_prediction(student_id):
        """Prépare les données d'un étudiant pour la prédiction"""
        query = """
            SELECT 
                g.score,
                g.subject_id,
                s.name as subject_name
            FROM grades g
            JOIN subjects s ON g.subject_id = s.id
            WHERE g.student_id = %s
        """
        results = Database.execute_query(query, (student_id,), fetch=True)
        
        if not results:
            return None
        
        df = pd.DataFrame([dict(row) for row in results])
        
        # Calculer les statistiques
        stats = {
            'avg_score': df['score'].mean(),
            'std_score': df['score'].std() if len(df) > 1 else 0,
            'min_score': df['score'].min(),
            'max_score': df['score'].max(),
            'num_grades': len(df)
        }
        
        return stats
