# Script de génération de dataset pour l'entraînement ML
import sys
import os
import random
import bcrypt
from datetime import datetime, timedelta

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import Database

# Listes de noms camerounais
PRENOMS_HOMMES = [
    "Jean", "Paul", "Pierre", "Jacques", "André", "Michel", "François", "Louis",
    "Emmanuel", "Daniel", "David", "Samuel", "Joseph", "Marc", "Luc", "Thomas",
    "Alain", "Bernard", "Claude", "Denis", "Eric", "Georges", "Henri", "Olivier",
    "Patrick", "Philippe", "Robert", "Serge", "Vincent", "Yves", "Amadou", "Moussa",
    "Ibrahim", "Abdoulaye", "Mamadou", "Ousmane", "Saidou", "Bouba", "Hamadou"
]

PRENOMS_FEMMES = [
    "Marie", "Anne", "Sophie", "Catherine", "Françoise", "Monique", "Jeanne",
    "Christine", "Isabelle", "Sylvie", "Nathalie", "Véronique", "Martine",
    "Brigitte", "Nicole", "Jacqueline", "Hélène", "Agnès", "Cécile", "Dominique",
    "Florence", "Laurence", "Valérie", "Sandrine", "Stéphanie", "Aminata", "Fatima",
    "Aissatou", "Mariama", "Fatoumata", "Kadiatou", "Oumou", "Rokia"
]

NOMS = [
    "Mbarga", "Ngo", "Kamga", "Kouam", "Tchoua", "Fotso", "Nguema", "Ondoa",
    "Abega", "Messi", "Eto'o", "Song", "Makoun", "Bassong", "Matip", "Choupo",
    "Moukoko", "Ekambi", "Toko", "Njie", "Manga", "Oyongo", "Ngadeu", "Onana",
    "Fai", "Kunde", "Zambo", "Hongla", "Bahoken", "Ngamaleu", "Bassogog",
    "Djoum", "Siani", "Omossola", "Tadjo", "Youmbi", "Zang", "Bella", "Ebelle",
    "Fouda", "Kana", "Mbia", "Njoya", "Owona", "Simo", "Tchamba", "Wome"
]

DEPARTEMENTS = ["Informatique", "Génie Civil", "Génie Mécanique", "Génie Électrique", "Sciences"]
NIVEAUX = ["L1", "L2", "L3", "M1", "M2"]

def generate_realistic_grades(student_level, num_subjects=6):
    """
    Génère des notes réalistes selon le profil de l'étudiant
    - Excellent: moyenne 14-18
    - Bon: moyenne 12-14
    - Moyen: moyenne 10-12
    - Faible: moyenne 7-10
    - Très faible: moyenne 4-7
    """
    profiles = {
        'excellent': (14, 18, 0.8),    # (min, max, std_dev)
        'bon': (12, 14, 1.0),
        'moyen': (10, 12, 1.2),
        'faible': (7, 10, 1.5),
        'tres_faible': (4, 7, 1.0)
    }
    
    # Distribution réaliste des profils
    profile_weights = [0.15, 0.25, 0.35, 0.20, 0.05]  # excellent, bon, moyen, faible, très faible
    profile = random.choices(list(profiles.keys()), weights=profile_weights)[0]
    
    min_score, max_score, std_dev = profiles[profile]
    
    grades = []
    for _ in range(num_subjects):
        # Générer une note avec variation
        base_score = random.uniform(min_score, max_score)
        variation = random.gauss(0, std_dev)
        score = max(0, min(20, base_score + variation))
        
        # Arrondir à 0.5
        score = round(score * 2) / 2
        grades.append(score)
    
    return grades

def generate_dataset(num_students=500):
    """Génère un dataset complet d'étudiants avec leurs notes"""
    
    print("=" * 60)
    print(f"Génération de {num_students} étudiants avec leurs notes")
    print("=" * 60)
    
    try:
        # Récupérer l'enseignant existant
        teacher_query = "SELECT id FROM users WHERE role = 'teacher' LIMIT 1"
        teacher = Database.execute_query_one(teacher_query)
        
        if not teacher:
            print("❌ Aucun enseignant trouvé. Exécutez d'abord init_db.py")
            return False
        
        teacher_id = teacher['id']
        print(f"✅ Enseignant trouvé (ID: {teacher_id})")
        
        # Récupérer les matières existantes
        subjects_query = "SELECT id FROM subjects"
        subjects = Database.execute_query(subjects_query, fetch=True)
        
        if not subjects or len(subjects) < 4:
            print("❌ Pas assez de matières. Exécutez d'abord init_db.py")
            return False
        
        subject_ids = [dict(s)['id'] for s in subjects]
        print(f"✅ {len(subject_ids)} matières trouvées")
        
        # Générer les étudiants
        print(f"\n📊 Génération de {num_students} étudiants...")
        
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        password_hash = bcrypt.hashpw("student123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        students_created = 0
        grades_created = 0
        
        for i in range(num_students):
            # Générer un nom aléatoire
            genre = random.choice(['M', 'F'])
            prenom = random.choice(PRENOMS_HOMMES if genre == 'M' else PRENOMS_FEMMES)
            nom = random.choice(NOMS)
            email = f"etudiant{i+1000}@enspd.cm"
            
            # Créer l'utilisateur
            try:
                cursor.execute("""
                    INSERT INTO users (email, password_hash, first_name, last_name, role)
                    VALUES (%s, %s, %s, %s, 'student')
                    RETURNING id
                """, (email, password_hash, prenom, nom))
                
                user_result = cursor.fetchone()
                user_id = user_result[0]
                
                # Créer le profil étudiant
                student_id = f"ENSPD2024{1000 + i:04d}"
                department = random.choice(DEPARTEMENTS)
                level = random.choice(NIVEAUX)
                
                cursor.execute("""
                    INSERT INTO student_profiles (user_id, student_id, department, level, academic_year)
                    VALUES (%s, %s, %s, %s, '2024-2025')
                """, (user_id, student_id, department, level))
                
                students_created += 1
                
                # Générer les notes
                grades = generate_realistic_grades(level, len(subject_ids))
                
                for subject_id, score in zip(subject_ids, grades):
                    cursor.execute("""
                        INSERT INTO grades (student_id, subject_id, grade_type, score, semester, academic_year)
                        VALUES (%s, %s, 'Examen', %s, 'S1', '2024-2025')
                    """, (user_id, subject_id, score))
                    grades_created += 1
                
                # Commit tous les 50 étudiants
                if (i + 1) % 50 == 0:
                    conn.commit()
                    print(f"  ✓ {i + 1}/{num_students} étudiants créés...")
            
            except Exception as e:
                print(f"  ⚠️ Erreur pour l'étudiant {i+1}: {e}")
                conn.rollback()
                continue
        
        # Commit final
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ Génération terminée avec succès!")
        print(f"   📊 Étudiants créés: {students_created}")
        print(f"   📝 Notes créées: {grades_created}")
        print(f"   📈 Moyenne de notes par étudiant: {grades_created / students_created:.1f}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Générer un dataset pour ENSPD LearnAI')
    parser.add_argument('--students', type=int, default=500, help='Nombre d\'étudiants à générer (défaut: 500)')
    
    args = parser.parse_args()
    
    print("\n🎓 ENSPD LearnAI - Générateur de Dataset")
    print(f"Nombre d'étudiants: {args.students}\n")
    
    success = generate_dataset(args.students)
    
    if success:
        print("\n🚀 Vous pouvez maintenant entraîner le modèle ML:")
        print("   python ml/train_model.py")
    else:
        print("\n❌ La génération a échoué. Vérifiez les erreurs ci-dessus.")
