"""
Routes d'administration temporaires pour le débogage
À SUPPRIMER EN PRODUCTION!
"""
from flask import Blueprint, jsonify, request
import bcrypt
from models.database import Database

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/reset-passwords', methods=['POST'])
def reset_passwords():
    """Réinitialiser les mots de passe - TEMPORAIRE POUR DEBUG"""
    
    # Mot de passe secret pour protéger cette route
    secret = request.json.get('secret')
    if secret != 'reset-learnai-2025':
        return jsonify({"error": "Non autorisé"}), 403
    
    # Nouveau mot de passe
    new_password = "password123"
    password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Liste des utilisateurs à mettre à jour
    users_to_update = [
        "etudiant1@enspd.cm",
        "etudiant2@enspd.cm",
        "etudiant3@enspd.cm",
        "enseignant@enspd.cm",
        "christianouragan@gmail.com"
    ]
    
    updated = []
    for email in users_to_update:
        try:
            query = "UPDATE users SET password_hash = %s WHERE email = %s"
            Database.execute_query(query, (password_hash, email))
            updated.append(email)
        except Exception as e:
            print(f"Erreur pour {email}: {e}")
    
    return jsonify({
        "message": "Mots de passe réinitialisés",
        "updated": updated,
        "password": new_password
    }), 200

@admin_bp.route('/test-jwt', methods=['GET'])
def test_jwt():
    """Tester la configuration JWT"""
    from config import Config
    
    return jsonify({
        "jwt_secret_key_configured": bool(Config.JWT_SECRET_KEY),
        "jwt_secret_key_length": len(Config.JWT_SECRET_KEY) if Config.JWT_SECRET_KEY else 0,
        "secret_key_configured": bool(Config.SECRET_KEY),
        "db_configured": bool(Config.DB_HOST and Config.DB_NAME)
    }), 200

@admin_bp.route('/test-token', methods=['POST'])
def test_token():
    """Tester un token JWT"""
    import jwt as pyjwt
    from config import Config
    
    data = request.json
    token = data.get('token')
    
    if not token:
        return jsonify({"error": "Token requis"}), 400
    
    try:
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
        return jsonify({
            "valid": True,
            "payload": payload,
            "user_id": payload.get('sub')
        }), 200
    except pyjwt.ExpiredSignatureError:
        return jsonify({"valid": False, "error": "Token expiré"}), 200
    except pyjwt.InvalidTokenError as e:
        return jsonify({"valid": False, "error": f"Token invalide: {str(e)}"}), 200
    except Exception as e:
        return jsonify({"valid": False, "error": f"Erreur: {str(e)}"}), 200

@admin_bp.route('/test-dashboard/<int:user_id>', methods=['GET'])
def test_dashboard(user_id):
    """Tester le dashboard sans JWT"""
    try:
        # Récupérer les notes
        query_grades = """
            SELECT g.*, s.name as subject_name, s.code as subject_code
            FROM grades g
            JOIN subjects s ON g.subject_id = s.id
            WHERE g.student_id = %s
            ORDER BY g.created_at DESC
            LIMIT 10
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
            "user_id": user_id,
            "grades_count": len(list(grades)) if grades else 0,
            "grades": [dict(g) for g in grades][:5] if grades else [],
            "statistics": dict(stats) if stats else {}
        }), 200
    except Exception as e:
        import traceback
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500
