# Routes pour les étudiants
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.database import Database
from ml.prediction_model import PredictionModel
from ml.recommendation_engine import RecommendationEngine

student_bp = Blueprint('student', __name__, url_prefix='/api/student')

@student_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """Récupère les données du tableau de bord étudiant"""
    user_id = get_jwt_identity()
    
    # Récupérer les notes
    query_grades = """
        SELECT g.*, s.name as subject_name, s.code as subject_code
        FROM grades g
        JOIN subjects s ON g.subject_id = s.id
        WHERE g.student_id = %s
        ORDER BY g.created_at DESC
    """
    grades = Database.execute_query(query_grades, (user_id,), fetch=True)
    
    # Calculer les statistiques
    query_stats = """
        SELECT 
            AVG(score) as avg_score,
            MIN(score) as min_score,
            MAX(score) as max_score,
            COUNT(*) as total_grades
        FROM grades
        WHERE student_id = %s
    """
    stats = Database.execute_query_one(query_stats, (user_id,))
    
    return jsonify({
        "grades": [dict(g) for g in grades] if grades else [],
        "statistics": dict(stats) if stats else {}
    }), 200

@student_bp.route('/predictions', methods=['GET'])
@jwt_required()
def get_predictions():
    """Récupère les prédictions IA pour l'étudiant avec messages personnalisés"""
    user_id = get_jwt_identity()
    
    try:
        model = PredictionModel()
        prediction = model.predict_success(user_id)
        
        if not prediction:
            return jsonify({"message": "Pas assez de données pour la prédiction"}), 200
        
        # Ajouter un message personnalisé basé sur la moyenne
        query_avg = "SELECT AVG(score) as avg_score FROM grades WHERE student_id = %s"
        result = Database.execute_query_one(query_avg, (user_id,))
        
        if result and result['avg_score']:
            avg = float(result['avg_score'])
            prediction['average_score'] = round(avg, 2)
            prediction['performance_message'] = get_performance_message(avg)
        
        return jsonify(prediction), 200
    except Exception as e:
        print(f"Erreur prédiction pour user {user_id}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"message": "Erreur lors de la prédiction", "error": str(e)}), 200

def get_performance_message(avg):
    """Génère un message personnalisé selon la moyenne"""
    if avg >= 18:
        return {
            "title": "Excellence académique",
            "emoji": "🏆",
            "message": "Performances exceptionnelles ! Vous êtes parmi les meilleurs.",
            "advice": "Continuez à viser l'excellence et inspirez vos camarades.",
            "level": "excellent"
        }
    elif avg >= 16:
        return {
            "title": "Très bonnes performances",
            "emoji": "⭐",
            "message": "Excellent travail ! Vous maîtrisez bien vos matières.",
            "advice": "Maintenez cette dynamique pour atteindre l'excellence.",
            "level": "very_good"
        }
    elif avg >= 14:
        return {
            "title": "Bonnes performances",
            "emoji": "✅",
            "message": "Vous êtes sur la bonne voie !",
            "advice": "Continuez vos efforts et visez encore plus haut.",
            "level": "good"
        }
    elif avg >= 12:
        return {
            "title": "Performances satisfaisantes",
            "emoji": "👍",
            "message": "Vous êtes dans la moyenne supérieure.",
            "advice": "Avec plus de travail régulier, vous pouvez atteindre de très bons résultats.",
            "level": "satisfactory"
        }
    elif avg >= 10:
        return {
            "title": "Performances moyennes",
            "emoji": "⚡",
            "message": "Vous validez vos matières mais pouvez faire mieux.",
            "advice": "Identifiez vos points faibles et travaillez-les régulièrement.",
            "level": "average"
        }
    elif avg >= 9:
        return {
            "title": "Attention requise",
            "emoji": "⚠️",
            "message": "Vous êtes juste en dessous de la moyenne.",
            "advice": "Redoublez d'efforts, consultez vos enseignants et utilisez le chatbot.",
            "level": "warning"
        }
    elif avg >= 8:
        return {
            "title": "Situation préoccupante",
            "emoji": "🚨",
            "message": "Vos résultats sont faibles. Il est urgent de réagir.",
            "advice": "Assistez aux cours de soutien, travaillez régulièrement et demandez de l'aide.",
            "level": "concerning"
        }
    else:
        return {
            "title": "Risque d'échec élevé",
            "emoji": "❌",
            "message": "Situation critique !",
            "advice": "Consultez immédiatement vos enseignants et suivez un plan de rattrapage.",
            "level": "critical"
        }

@student_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    """Récupère les recommandations de ressources"""
    user_id = get_jwt_identity()
    
    # Augmenter la limite pour avoir plus de recommandations
    recommendations = RecommendationEngine.recommend_resources(user_id, limit=50)
    
    return jsonify({"recommendations": recommendations}), 200

@student_bp.route('/debug/grades', methods=['GET'])
@jwt_required()
def debug_grades():
    """Debug: Affiche toutes les notes et moyennes par matière"""
    user_id = get_jwt_identity()
    
    # Récupérer toutes les notes
    query_all = """
        SELECT g.*, s.name as subject_name
        FROM grades g
        JOIN subjects s ON g.subject_id = s.id
        WHERE g.student_id = %s
        ORDER BY s.name, g.created_at DESC
    """
    all_grades = Database.execute_query(query_all, (user_id,), fetch=True)
    
    # Calculer les moyennes par matière
    query_avg = """
        SELECT 
            s.name as subject_name,
            AVG(g.score) as avg_score,
            COUNT(g.id) as total_grades
        FROM grades g
        JOIN subjects s ON g.subject_id = s.id
        WHERE g.student_id = %s
        GROUP BY s.name
        ORDER BY avg_score ASC
    """
    averages = Database.execute_query(query_avg, (user_id,), fetch=True)
    
    return jsonify({
        "all_grades": [dict(g) for g in all_grades] if all_grades else [],
        "averages": [dict(a) for a in averages] if averages else []
    }), 200
