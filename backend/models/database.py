# Gestionnaire de connexion à la base de données PostgreSQL
import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

class Database:
    """Classe pour gérer les connexions à PostgreSQL"""
    
    @staticmethod
    def get_connection():
        """Établit une connexion à la base de données"""
        try:
            conn = psycopg2.connect(
                dbname=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                host=Config.DB_HOST,
                port=Config.DB_PORT
            )
            return conn
        except psycopg2.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            raise
    
    @staticmethod
    def execute_query(query, params=None, fetch=False):
        """Exécute une requête SQL"""
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            
            conn.commit()
            return cursor.rowcount
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            print(f"Erreur d'exécution de requête: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def execute_query_one(query, params=None):
        """Exécute une requête et retourne un seul résultat"""
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            return result
        except psycopg2.Error as e:
            print(f"Erreur d'exécution de requête: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
