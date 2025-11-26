"""
Script d'initialisation de la base de données
Exécuté automatiquement au démarrage de l'application
"""
import os
import psycopg2
from psycopg2 import sql
from config import Config

def get_db_connection():
    """Créer une connexion à la base de données"""
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        return conn
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        return None

def init_database():
    """Initialiser la base de données avec le schéma"""
    print("🔄 Initialisation de la base de données...")
    
    # Vérifier si les variables d'environnement DB sont définies
    if not all([Config.DB_HOST, Config.DB_NAME, Config.DB_USER, Config.DB_PASSWORD]):
        print("⚠️  Variables de base de données non configurées. Utilisation en mode sans BD.")
        return False
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Lire le fichier schema.sql
        schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'schema.sql')
        
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            # Exécuter le schéma
            cursor.execute(schema_sql)
            conn.commit()
            print("✅ Base de données initialisée avec succès!")
            
            # Vérifier les tables créées
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            print(f"📊 Tables créées: {', '.join([t[0] for t in tables])}")
            
        else:
            print(f"⚠️  Fichier schema.sql non trouvé: {schema_path}")
            return False
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def check_database_exists():
    """Vérifier si la base de données est déjà initialisée"""
    if not all([Config.DB_HOST, Config.DB_NAME, Config.DB_USER, Config.DB_PASSWORD]):
        return False
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'users'
            );
        """)
        exists = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return exists
    except:
        if conn:
            conn.close()
        return False

if __name__ == "__main__":
    # Exécution directe du script
    if check_database_exists():
        print("✅ Base de données déjà initialisée")
    else:
        init_database()
