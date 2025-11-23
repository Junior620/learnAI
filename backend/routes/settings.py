# Routes pour la gestion des paramètres utilisateur
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.database import Database
import bcrypt

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/api/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Récupérer le profil de l'utilisateur connecté"""
    try:
        current_user_id = get_jwt_identity()
        user = User.get_user_by_id(current_user_id)
        
        if not user:
            return jsonify({'message': 'Utilisateur non trouvé'}), 404
        
        # Supprimer le hash du mot de passe
        user.pop('password_hash', None)
        
        return jsonify({'user': user}), 200
    except Exception as e:
        print(f"Erreur get_profile: {e}")
        return jsonify({'message': 'Erreur serveur'}), 500


@settings_bp.route('/api/auth/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Mettre à jour le profil utilisateur"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        user_id = current_user_id
        
        # Récupérer le rôle de l'utilisateur
        user = User.get_user_by_id(user_id)
        if not user:
            return jsonify({'message': 'Utilisateur non trouvé'}), 404
        
        # Mettre à jour les informations de base
        query = """
            UPDATE users 
            SET first_name = %s, last_name = %s, email = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING id, email, first_name, last_name, role
        """
        
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(query, (
            data.get('first_name'),
            data.get('last_name'),
            data.get('email'),
            user_id
        ))
        
        result = cursor.fetchone()
        
        # Si c'est un étudiant, mettre à jour le profil étudiant
        if user['role'] == 'student' and 'student_profile' in data:
            profile = data['student_profile']
            
            # Vérifier si le profil existe
            cursor.execute("SELECT id FROM student_profiles WHERE user_id = %s", (user_id,))
            existing_profile = cursor.fetchone()
            
            if existing_profile:
                # Mettre à jour
                update_query = """
                    UPDATE student_profiles 
                    SET student_id = %s, department = %s, level = %s, academic_year = %s
                    WHERE user_id = %s
                """
                cursor.execute(update_query, (
                    profile.get('student_id'),
                    profile.get('department'),
                    profile.get('level'),
                    profile.get('academic_year'),
                    user_id
                ))
            else:
                # Créer
                insert_query = """
                    INSERT INTO student_profiles (user_id, student_id, department, level, academic_year)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    user_id,
                    profile.get('student_id'),
                    profile.get('department'),
                    profile.get('level'),
                    profile.get('academic_year')
                ))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        if result:
            user_data = {
                'id': result[0],
                'email': result[1],
                'first_name': result[2],
                'last_name': result[3],
                'role': result[4]
            }
            return jsonify({
                'message': 'Profil mis à jour avec succès',
                'user': user_data
            }), 200
        else:
            return jsonify({'message': 'Erreur lors de la mise à jour'}), 400
            
    except Exception as e:
        print(f"Erreur update_profile: {e}")
        return jsonify({'message': 'Erreur serveur'}), 500


@settings_bp.route('/api/students/<int:user_id>/profile', methods=['GET'])
@jwt_required()
def get_student_profile(user_id):
    """Récupérer le profil étudiant"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.get_user_by_id(current_user_id)
        
        # Vérifier que l'utilisateur accède à son propre profil
        if current_user_id != user_id and current_user['role'] != 'admin':
            return jsonify({'message': 'Accès non autorisé'}), 403
        
        query = """
            SELECT student_id, department, level, academic_year, created_at
            FROM student_profiles
            WHERE user_id = %s
        """
        
        result = Database.execute_query_one(query, (user_id,))
        
        if result:
            profile = {
                'student_id': result[0],
                'department': result[1],
                'level': result[2],
                'academic_year': result[3],
                'created_at': result[4]
            }
            return jsonify({'profile': profile}), 200
        else:
            return jsonify({'profile': None}), 200
            
    except Exception as e:
        print(f"Erreur get_student_profile: {e}")
        return jsonify({'message': 'Erreur serveur'}), 500


@settings_bp.route('/api/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Changer le mot de passe"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'message': 'Tous les champs sont requis'}), 400
        
        # Vérifier le mot de passe actuel
        user = User.get_user_by_id(current_user_id)
        
        if not user or not User.verify_password(current_password, user['password_hash']):
            return jsonify({'message': 'Mot de passe actuel incorrect'}), 401
        
        # Hasher le nouveau mot de passe
        new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Mettre à jour le mot de passe
        query = "UPDATE users SET password_hash = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (new_password_hash, current_user_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Mot de passe changé avec succès'}), 200
        
    except Exception as e:
        print(f"Erreur change_password: {e}")
        return jsonify({'message': 'Erreur serveur'}), 500


@settings_bp.route('/api/auth/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    """Supprimer le compte utilisateur"""
    try:
        user_id = get_jwt_identity()
        
        # Supprimer l'utilisateur (CASCADE supprimera les données liées)
        query = "DELETE FROM users WHERE id = %s"
        
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Compte supprimé avec succès'}), 200
        
    except Exception as e:
        print(f"Erreur delete_account: {e}")
        return jsonify({'message': 'Erreur serveur'}), 500
