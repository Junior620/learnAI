# Routes d'authentification
from flask import Blueprint, request, jsonify
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Endpoint d'inscription"""
    data = request.get_json()
    
    # Validation
    required_fields = ['email', 'password', 'first_name', 'last_name', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Champs manquants"}), 400
    
    # Données étudiant si applicable
    student_data = None
    if data['role'] == 'student':
        student_data = {
            'student_id': data.get('student_id'),
            'department': data.get('department'),
            'level': data.get('level'),
            'academic_year': data.get('academic_year', '2024-2025')
        }
    
    result, status = AuthService.register_user(
        data['email'],
        data['password'],
        data['first_name'],
        data['last_name'],
        data['role'],
        student_data
    )
    
    return jsonify(result), status

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint de connexion"""
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email et mot de passe requis"}), 400
    
    result, status = AuthService.login_user(data['email'], data['password'])
    return jsonify(result), status
