# Moteur de recommandation de ressources
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from models.database import Database

class RecommendationEngine:
    """Moteur de recommandation basé sur le contenu et les performances"""
    
    @staticmethod
    def get_student_weak_subjects(student_id, threshold=12):
        """Identifie les matières faibles d'un étudiant
        
        Args:
            student_id: ID de l'étudiant
            threshold: Seuil de moyenne (par défaut 12, pour inclure les performances moyennes)
        
        Returns:
            Liste des matières avec moyenne < threshold, triées par moyenne croissante
        """
        query = """
            SELECT 
                s.id as subject_id,
                s.name as subject_name,
                s.code as subject_code,
                AVG(g.score) as avg_score,
                COUNT(g.id) as total_grades,
                MIN(g.score) as min_score,
                MAX(g.score) as max_score
            FROM grades g
            JOIN subjects s ON g.subject_id = s.id
            WHERE g.student_id = %s
            GROUP BY s.id, s.name, s.code
            HAVING AVG(g.score) < %s
            ORDER BY avg_score ASC
        """
        results = Database.execute_query(query, (student_id, threshold), fetch=True)
        weak_subjects = [dict(row) for row in results] if results else []
        
        # Debug: afficher les matières faibles détectées
        if weak_subjects:
            print(f"🔍 Matières faibles détectées pour l'étudiant {student_id}:")
            for subject in weak_subjects:
                print(f"   - {subject['subject_name']}: {subject['avg_score']:.2f}/20")
        else:
            print(f"ℹ️ Aucune matière faible (< {threshold}) pour l'étudiant {student_id}")
        
        return weak_subjects
    
    @staticmethod
    def recommend_resources(student_id, limit=50):
        """Recommande des ressources intelligemment pour un étudiant
        
        Stratégie:
        1. Identifier les matières faibles (moyenne < 12)
        2. Prioriser les matières les plus faibles
        3. Adapter le niveau de difficulté selon la moyenne
        4. Si pas de matières faibles, recommander des ressources générales
        """
        weak_subjects = RecommendationEngine.get_student_weak_subjects(student_id, threshold=12)
        
        if not weak_subjects:
            # Si pas de matières faibles, recommander des ressources générales
            query = """
                SELECT r.*, s.name as subject_name, s.code as subject_code
                FROM resources r
                LEFT JOIN subjects s ON r.subject_id = s.id
                ORDER BY r.created_at DESC
                LIMIT %s
            """
            results = Database.execute_query(query, (limit,), fetch=True)
            recommendations = [dict(row) for row in results] if results else []
            
            # Sauvegarder avec raison générale
            for rec in recommendations:
                RecommendationEngine.save_recommendation(
                    student_id,
                    rec['id'],
                    rec.get('subject_id'),
                    0.70,
                    "Ressource recommandée pour enrichir vos connaissances"
                )
        else:
            # Recommander des ressources pour les matières faibles
            recommendations = []
            
            for subject in weak_subjects[:5]:  # Top 5 matières les plus faibles
                avg_score = float(subject['avg_score'])
                subject_id = subject['subject_id']
                subject_name = subject['subject_name']
                
                # Déterminer le niveau de difficulté approprié
                if avg_score < 8:
                    difficulty = 'beginner'
                    reason = f"Matière critique ({avg_score:.1f}/20) - Commencez par les bases"
                    score = 0.95
                elif avg_score < 10:
                    difficulty = 'beginner'
                    reason = f"Matière faible ({avg_score:.1f}/20) - Renforcez vos bases"
                    score = 0.90
                elif avg_score < 12:
                    difficulty = 'intermediate'
                    reason = f"Matière à améliorer ({avg_score:.1f}/20) - Progressez vers l'excellence"
                    score = 0.85
                else:
                    difficulty = 'intermediate'
                    reason = f"Matière à consolider ({avg_score:.1f}/20)"
                    score = 0.80
                
                # Récupérer les ressources adaptées
                query = """
                    SELECT r.*, s.name as subject_name, s.code as subject_code
                    FROM resources r
                    JOIN subjects s ON r.subject_id = s.id
                    WHERE r.subject_id = %s 
                    AND (r.difficulty_level = %s OR r.difficulty_level IS NULL)
                    ORDER BY 
                        CASE 
                            WHEN r.difficulty_level = %s THEN 1
                            ELSE 2
                        END,
                        r.created_at DESC
                    LIMIT 3
                """
                results = Database.execute_query(
                    query, 
                    (subject_id, difficulty, difficulty), 
                    fetch=True
                )
                
                if results:
                    for row in results:
                        rec = dict(row)
                        rec['recommendation_reason'] = reason
                        rec['recommendation_score'] = score
                        rec['subject_avg_score'] = avg_score
                        recommendations.append(rec)
                        
                        # Sauvegarder la recommandation
                        RecommendationEngine.save_recommendation(
                            student_id,
                            rec['id'],
                            subject_id,
                            score,
                            reason
                        )
            
            # Limiter au nombre demandé
            recommendations = recommendations[:limit]
        
        return recommendations
    
    @staticmethod
    def save_recommendation(student_id, resource_id, subject_id, score, reason):
        """Sauvegarde une recommandation"""
        query = """
            INSERT INTO recommendations (student_id, resource_id, subject_id, recommendation_score, reason)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """
        Database.execute_query(query, (student_id, resource_id, subject_id, score, reason))
