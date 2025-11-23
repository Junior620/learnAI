# Tests unitaires pour l'authentification
import unittest
import sys
sys.path.append('../backend')

from services.auth_service import AuthService
from models.user import User

class TestAuthentication(unittest.TestCase):
    """Tests pour le système d'authentification"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.test_email = "test@enspd.cm"
        self.test_password = "testpassword123"
    
    def test_password_hashing(self):
        """Test du hachage de mot de passe"""
        import bcrypt
        password = "testpassword"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Vérifier que le hash est différent du mot de passe
        self.assertNotEqual(password, hashed)
        
        # Vérifier que la vérification fonctionne
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed))
    
    def test_user_registration_validation(self):
        """Test de validation lors de l'inscription"""
        # Test avec données manquantes
        result, status = AuthService.register_user(
            email="",
            password="test",
            first_name="Test",
            last_name="User",
            role="student"
        )
        
        # Devrait échouer avec email vide
        self.assertIn("error", result)
    
    def test_login_validation(self):
        """Test de validation lors de la connexion"""
        # Test avec email inexistant
        result, status = AuthService.login_user(
            "nonexistent@enspd.cm",
            "password"
        )
        
        self.assertEqual(status, 401)
        self.assertIn("error", result)

class TestUserModel(unittest.TestCase):
    """Tests pour le modèle User"""
    
    def test_password_verification(self):
        """Test de vérification de mot de passe"""
        import bcrypt
        password = "testpassword"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Test avec bon mot de passe
        self.assertTrue(User.verify_password(password, password_hash))
        
        # Test avec mauvais mot de passe
        self.assertFalse(User.verify_password("wrongpassword", password_hash))

if __name__ == '__main__':
    unittest.main()
