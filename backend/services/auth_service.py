# Service d'authentification avec JWT
from flask_jwt_extended import create_access_token
from models.user import User

class AuthService:
    """Service pour gérer l'authentification"""
    
    @staticmethod
    def register_user(email, password, first_name, last_name, role, student_data=None):
        """Enregistre un nouvel utilisateur"""
        # Vérifier si l'utilisateur existe déjà
        existing_user = User.get_user_by_email(email)
        if existing_user:
            return {"error": "Un utilisateur avec cet email existe déjà"}, 400
        
        # Créer l'utilisateur
        user = User.create_user(email, password, first_name, last_name, role)
        if not user:
            return {"error": "Erreur lors de la création de l'utilisateur"}, 500
        
        # Si c'est un étudiant, créer le profil
        if role == 'student' and student_data:
            User.create_student_profile(
                user['id'],
                student_data.get('student_id'),
                student_data.get('department'),
                student_data.get('level'),
                student_data.get('academic_year')
            )
        
        # Générer le token JWT
        access_token = create_access_token(identity=user['id'])
        
        return {
            "message": "Utilisateur créé avec succès",
            "user": user,
            "access_token": access_token
        }, 201
    
    @staticmethod
    def login_user(email, password):
        """Authentifie un utilisateur"""
        # Récupérer l'utilisateur
        user = User.get_user_by_email(email)
        if not user:
            return {"error": "Email ou mot de passe incorrect"}, 401
        
        # Vérifier le mot de passe
        if not User.verify_password(password, user['password_hash']):
            return {"error": "Email ou mot de passe incorrect"}, 401
        
        # Générer le token JWT
        access_token = create_access_token(identity=user['id'])
        
        # Retirer le hash du mot de passe
        user.pop('password_hash', None)
        
        return {
            "message": "Connexion réussie",
            "user": user,
            "access_token": access_token
        }, 200
