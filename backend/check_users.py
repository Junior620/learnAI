"""
Vérifier les utilisateurs dans la base
"""
from models.database import Database

def check_users():
    print("👥 Vérification des utilisateurs...\n")
    
    # Compter les utilisateurs
    query = "SELECT COUNT(*) as count FROM users"
    result = Database.execute_query_one(query)
    print(f"📊 Total utilisateurs: {result['count']}")
    
    # Lister les 10 premiers
    query = "SELECT id, email, first_name, last_name, role FROM users LIMIT 10"
    users = Database.execute_query(query, fetch=True)
    
    print("\n📋 Premiers utilisateurs:")
    for user in users:
        print(f"   {user['id']}: {user['email']} - {user['first_name']} {user['last_name']} ({user['role']})")
    
    # Chercher student1
    query = "SELECT * FROM users WHERE email LIKE '%student1%'"
    students = Database.execute_query(query, fetch=True)
    
    print(f"\n🔍 Utilisateurs avec 'student1' dans l'email: {len(list(students)) if students else 0}")
    if students:
        for student in students:
            print(f"   {student['email']}")

if __name__ == "__main__":
    check_users()
