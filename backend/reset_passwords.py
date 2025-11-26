"""
Réinitialiser les mots de passe des utilisateurs de test
"""
import bcrypt
from models.database import Database

def reset_passwords():
    print("🔐 Réinitialisation des mots de passe...\n")
    
    # Nouveau mot de passe
    new_password = "password123"
    password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Liste des utilisateurs à mettre à jour
    users_to_update = [
        "etudiant1@enspd.cm",
        "etudiant2@enspd.cm",
        "etudiant3@enspd.cm",
        "enseignant@enspd.cm",
        "christianouragan@gmail.com"
    ]
    
    for email in users_to_update:
        try:
            query = "UPDATE users SET password_hash = %s WHERE email = %s"
            Database.execute_query(query, (password_hash, email))
            print(f"✅ Mot de passe mis à jour pour: {email}")
        except Exception as e:
            print(f"❌ Erreur pour {email}: {e}")
    
    print(f"\n✅ Mots de passe réinitialisés!")
    print(f"📧 Email: un des emails ci-dessus")
    print(f"🔑 Mot de passe: {new_password}")

if __name__ == "__main__":
    reset_passwords()
