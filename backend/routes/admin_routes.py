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
