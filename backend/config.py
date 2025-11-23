# Configuration de l'application ENSPD LearnAI
import os
from datetime import timedelta

class Config:
    """Configuration principale de l'application"""
    
    # Base de données PostgreSQL
    DB_NAME = os.getenv("DB_NAME", "learnai")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-secret-key-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Groq API (Recommandé - Plus rapide et gratuit)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-in-production")
    DEBUG = os.getenv("DEBUG", "True") == "True"
    
    # ML Models
    MODEL_PATH = "ml/models/"
    DATA_PATH = "ml/data/"
    
    @staticmethod
    def get_db_connection_string():
        """Retourne la chaîne de connexion PostgreSQL"""
        return f"dbname={Config.DB_NAME} user={Config.DB_USER} password={Config.DB_PASSWORD} host={Config.DB_HOST} port={Config.DB_PORT}"
