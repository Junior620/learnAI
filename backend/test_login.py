"""
Test du login pour diagnostiquer le problème
"""
from models.user import User
import bcrypt

def test_login():
    print("🧪 Test du login...\n")
    
    email = "etudiant1@enspd.cm"
    password = "password123"
    
    # Récupérer l'utilisateur
    print(f"📧 Recherche de l'utilisateur: {email}")
    user = User.get_user_by_email(email)
    
    if not user:
        print("❌ Utilisateur non trouvé!")
        return
    
    print(f"✅ Utilisateur trouvé: {user['first_name']} {user['last_name']}")
    print(f"   ID: {user['id']}")
    print(f"   Role: {user['role']}")
    print(f"   Hash: {user['password_hash'][:50]}...")
    
    # Tester le mot de passe
    print(f"\n🔐 Test du mot de passe: {password}")
    is_valid = User.verify_password(password, user['password_hash'])
    
    if is_valid:
        print("✅ Mot de passe correct!")
    else:
        print("❌ Mot de passe incorrect!")
        
        # Tester de créer un nouveau hash
        print("\n🔄 Création d'un nouveau hash pour comparaison...")
        new_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print(f"   Nouveau hash: {new_hash.decode()[:50]}...")
        
        # Tester avec le nouveau hash
        is_valid_new = bcrypt.checkpw(password.encode('utf-8'), new_hash)
        print(f"   Test avec nouveau hash: {'✅ OK' if is_valid_new else '❌ FAIL'}")

if __name__ == "__main__":
    test_login()
