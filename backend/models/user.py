# Modèle User pour la gestion des utilisateurs
import bcrypt
from models.database import Database

class User:
    """Modèle pour les utilisateurs (étudiants, enseignants, admin)"""
    
    @staticmethod
    def create_user(email, password, first_name, last_name, role):
        """Crée un nouvel utilisateur"""
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        query = """
            INSERT INTO users (email, password_hash, first_name, last_name, role)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, email, first_name, last_name, role, created_at
        """
        
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (email, password_hash, first_name, last_name, role))
            result = cursor.fetchone()
            conn.commit()
            
            if result:
                return {
                    'id': result[0],
                    'email': result[1],
                    'first_name': result[2],
                    'last_name': result[3],
                    'role': result[4],
                    'created_at': result[5]
                }
            return None
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Erreur création utilisateur: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def get_user_by_email(email):
        """Récupère un utilisateur par email"""
        query = "SELECT * FROM users WHERE email = %s"
        result = Database.execute_query_one(query, (email,))
        return dict(result) if result else None
    
    @staticmethod
    def get_user_by_id(user_id):
        """Récupère un utilisateur par ID"""
        query = "SELECT id, email, first_name, last_name, role, created_at FROM users WHERE id = %s"
        result = Database.execute_query_one(query, (user_id,))
        return dict(result) if result else None
    
    @staticmethod
    def verify_password(password, password_hash):
        """Vérifie le mot de passe"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    @staticmethod
    def get_all_students():
        """Récupère tous les étudiants"""
        query = """
            SELECT u.id, u.email, u.first_name, u.last_name, 
                   sp.student_id, sp.department, sp.level
            FROM users u
            LEFT JOIN student_profiles sp ON u.id = sp.user_id
            WHERE u.role = 'student'
            ORDER BY u.last_name, u.first_name
        """
        results = Database.execute_query(query, fetch=True)
        return [dict(row) for row in results] if results else []
    
    @staticmethod
    def create_student_profile(user_id, student_id, department, level, academic_year):
        """Crée un profil étudiant"""
        query = """
            INSERT INTO student_profiles (user_id, student_id, department, level, academic_year)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (user_id, student_id, department, level, academic_year))
            result = cursor.fetchone()
            conn.commit()
            
            if result:
                return {'id': result[0]}
            return None
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Erreur création profil étudiant: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
