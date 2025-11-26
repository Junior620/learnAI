# Routes pour les étudiants - Version sans JWT (contournement bug)
from flask import Blueprint, request, jsonify
from models.database import Database
from ml.prediction_model import PredictionModel
from ml.recommendation_engine import RecommendationEngine
import jwt as pyjwt
from config import Config

student_v2_bp = Blueprint('student_v2', __name__, url_prefix='/api/v2/student')

def verify_token():
    """Vérifier le token JWT manuellement"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        print("Pas de header Authorization")
        return None
    
    token = auth_header.split(' ')[1]
    try:
        # Décoder avec PyJWT directement
        # Désactiver toutes les vérifications sauf la signature et l'expiration
        payload = pyjwt.decode(
            token, 
            Config.JWT_SECRET_KEY, 
            algorithms=['HS256'],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_nbf": True,
                "verify_iat": True,
                "verify_aud": False,
                "require_exp": False,
                "require_iat": False,
                "require_nbf": False
            }
        )
        user_id = payload.get('sub')
        print(f"Token valide pour user_id: {user_id}")
        return user_id
    except pyjwt.ExpiredSignatureError:
        print("Token expiré")
        return None
    except pyjwt.InvalidTokenError as e:
        print(f"Token invalide: {e}")
        return None
    except Exception as e:
        print(f"Erreur vérification token: {e}")
        return None

@student_v2_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Récupère les données du tableau de bord étudiant"""
    user_id = verify_token()
    if not user_id:
        return jsonify({"error": "Non autorisé"}), 401
    
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

@student_v2_bp.route('/predictions', methods=['GET'])
def get_predictions():
    """Récupère les prédictions IA pour l'étudiant"""
    user_id = verify_token()
    if not user_id:
        return jsonify({"error": "Non autorisé"}), 401
    
    try:
        model = PredictionModel()
        prediction = model.predict_success(user_id)
        
        if not prediction:
            return jsonify({"message": "Pas assez de données pour la prédiction"}), 200
        
        # Ajouter un message personnalisé
        query_avg = "SELECT AVG(score) as avg_score FROM grades WHERE student_id = %s"
        result = Database.execute_query_one(query_avg, (user_id,))
        
        if result and result['avg_score']:
            avg = float(result['avg_score'])
            prediction['average_score'] = round(avg, 2)
            prediction['performance_message'] = get_performance_message(avg)
        
        return jsonify(prediction), 200
    except Exception as e:
        print(f"Erreur prédiction: {e}")
        return jsonify({"message": "Erreur lors de la prédiction"}), 200

@student_v2_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    """Récupère les recommandations de ressources"""
    user_id = verify_token()
    if not user_id:
        return jsonify({"error": "Non autorisé"}), 401
    
    recommendations = RecommendationEngine.recommend_resources(user_id, limit=50)
    return jsonify({"recommendations": recommendations}), 200

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
    else:
        return {
            "title": "Attention requise",
            "emoji": "⚠️",
            "message": "Vos résultats nécessitent une attention particulière.",
            "advice": "Consultez vos enseignants et utilisez les ressources disponibles.",
            "level": "warning"
        }
