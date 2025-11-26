# Application principale Flask - ENSPD LearnAI
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

# Import des routes
from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.teacher_routes import teacher_bp
from routes.chatbot_routes import chatbot_bp
from routes.grades_routes import grades_bp
from routes.settings import settings_bp

def create_app():
    """Factory pour créer l'application Flask"""
    app = Flask(__name__)
    
    # Initialiser la base de données au premier démarrage
    try:
        from init_db import check_database_exists, init_database
        if not check_database_exists():
            print("🔄 Première exécution - Initialisation de la base de données...")
            init_database()
    except Exception as e:
        print(f"⚠️  Impossible d'initialiser la BD: {e}")
    
    # Configuration
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.JWT_ACCESS_TOKEN_EXPIRES
    
    # CORS - Configuration complète
    CORS(app, 
         resources={r"/api/*": {"origins": "*"}},
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         supports_credentials=True)
    
    # JWT
    jwt = JWTManager(app)
    
    # Enregistrement des blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(grades_bp)
    app.register_blueprint(settings_bp)
    
    # Route de test
    @app.route('/')
    def index():
        return jsonify({
            "message": "ENSPD LearnAI API",
            "version": "1.0.0",
            "status": "running"
        })
    
    # Gestion des erreurs
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Route non trouvée"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Erreur serveur interne"}), 500
    
    return app

# Créer l'instance de l'app pour gunicorn
app = create_app()

if __name__ == '__main__':
    print("🚀 ENSPD LearnAI API démarrée sur http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)
