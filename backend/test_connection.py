"""
Script de test pour vérifier la connexion à la base de données
"""
import os
import psycopg2
from config import Config

def test_database_connection():
    """Tester la connexion à la base de données"""
    print("🔍 Test de connexion à la base de données...\n")
    
    # Afficher les variables (masquées)
    print(f"DB_HOST: {Config.DB_HOST}")
    print(f"DB_NAME: {Config.DB_NAME}")
    print(f"DB_USER: {Config.DB_USER}")
    print(f"DB_PORT: {Config.DB_PORT}")
    print(f"DB_PASSWORD: {'*' * len(Config.DB_PASSWORD) if Config.DB_PASSWORD else 'NON DÉFINI'}")
    print(f"SECRET_KEY: {'*' * len(Config.SECRET_KEY) if Config.SECRET_KEY else 'NON DÉFINI'}")
    print(f"JWT_SECRET_KEY: {'*' * len(Config.JWT_SECRET_KEY) if Config.JWT_SECRET_KEY else 'NON DÉFINI'}\n")
    
    # Tester la connexion
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        cursor = conn.cursor()
        
        # Tester une requête simple
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        print(f"✅ Connexion réussie!")
        print(f"✅ {count} utilisateurs dans la base")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()
