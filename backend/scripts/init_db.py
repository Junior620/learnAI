# Script d'initialisation de la base de données avec données de test
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import Database
from models.user import User
import bcrypt

def create_educational_resources(teacher_id):
    """Crée automatiquement des ressources pédagogiques pour toutes les matières"""
    
    # Récupérer toutes les matières
    subjects_query = "SELECT id, name, code FROM subjects ORDER BY id"
    subjects = Database.execute_query(subjects_query, fetch=True)
    
    if not subjects:
        print("⚠️ Aucune matière trouvée")
        return 0
    
    resources_data = []
    
    for subject in subjects:
        subject_id = subject['id']
        subject_name = subject['name']
        
        # Ressources pour chaque matière (7 par matière)
        resources_data.extend([
            # Niveau Débutant (3 ressources)
            {
                'title': f'Introduction à {subject_name}',
                'description': f'Cours complet pour débuter en {subject_name}. Couvre tous les concepts de base avec des exemples pratiques.',
                'resource_type': 'pdf',
                'url': f'https://example.com/cours/{subject_name.lower().replace(" ", "-")}-debutant.pdf',
                'subject_id': subject_id,
                'difficulty_level': 'beginner'
            },
            {
                'title': f'Tutoriel vidéo {subject_name} - Les bases',
                'description': f'Série de vidéos pour comprendre les fondamentaux de {subject_name}. Durée: 2h30.',
                'resource_type': 'video',
                'url': f'https://youtube.com/watch?v={subject_name[:5]}',
                'subject_id': subject_id,
                'difficulty_level': 'beginner'
            },
            {
                'title': f'Exercices de base en {subject_name}',
                'description': f'50 exercices corrigés pour maîtriser les bases de {subject_name}.',
                'resource_type': 'exercise',
                'url': f'https://example.com/exercices/{subject_name.lower().replace(" ", "-")}-base.pdf',
                'subject_id': subject_id,
                'difficulty_level': 'beginner'
            },
            
            # Niveau Intermédiaire (2 ressources)
            {
                'title': f'{subject_name} - Niveau intermédiaire',
                'description': f'Approfondissez vos connaissances en {subject_name} avec ce cours avancé.',
                'resource_type': 'pdf',
                'url': f'https://example.com/cours/{subject_name.lower().replace(" ", "-")}-intermediaire.pdf',
                'subject_id': subject_id,
                'difficulty_level': 'intermediate'
            },
            {
                'title': f'Problèmes résolus en {subject_name}',
                'description': f'Collection de problèmes types avec solutions détaillées en {subject_name}.',
                'resource_type': 'exercise',
                'url': f'https://example.com/exercices/{subject_name.lower().replace(" ", "-")}-intermediaire.pdf',
                'subject_id': subject_id,
                'difficulty_level': 'intermediate'
            },
            
            # Niveau Avancé (2 ressources)
            {
                'title': f'{subject_name} avancé - Préparation examens',
                'description': f'Ressources avancées pour exceller en {subject_name}. Sujets d\'examens corrigés.',
                'resource_type': 'pdf',
                'url': f'https://example.com/cours/{subject_name.lower().replace(" ", "-")}-avance.pdf',
                'subject_id': subject_id,
                'difficulty_level': 'advanced'
            },
            {
                'title': f'Projet pratique en {subject_name}',
                'description': f'Projet complet pour mettre en pratique vos compétences en {subject_name}.',
                'resource_type': 'exercise',
                'url': f'https://example.com/projets/{subject_name.lower().replace(" ", "-")}-projet.pdf',
                'subject_id': subject_id,
                'difficulty_level': 'advanced'
            }
        ])
    
    # Ajouter des ressources générales (sans matière spécifique)
    resources_data.extend([
        {
            'title': 'Méthodes de travail efficaces',
            'description': 'Guide complet pour améliorer vos méthodes de travail et votre organisation.',
            'resource_type': 'article',
            'url': 'https://example.com/methodes-travail.html',
            'subject_id': None,
            'difficulty_level': None
        },
        {
            'title': 'Gestion du stress aux examens',
            'description': 'Techniques pour gérer le stress et optimiser vos performances aux examens.',
            'resource_type': 'article',
            'url': 'https://example.com/gestion-stress.html',
            'subject_id': None,
            'difficulty_level': None
        },
        {
            'title': 'Techniques de mémorisation',
            'description': 'Méthodes scientifiquement prouvées pour améliorer votre mémoire.',
            'resource_type': 'video',
            'url': 'https://youtube.com/watch?v=memorisation',
            'subject_id': None,
            'difficulty_level': None
        },
        {
            'title': 'Organisation et planification',
            'description': 'Comment organiser votre temps et planifier vos révisions efficacement.',
            'resource_type': 'article',
            'url': 'https://example.com/organisation.html',
            'subject_id': None,
            'difficulty_level': None
        }
    ])
    
    # Insérer les ressources
    insert_query = """
        INSERT INTO resources (title, description, resource_type, url, subject_id, difficulty_level, created_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """
    
    count = 0
    for resource in resources_data:
        try:
            Database.execute_query(
                insert_query,
                (
                    resource['title'],
                    resource['description'],
                    resource['resource_type'],
                    resource['url'],
                    resource['subject_id'],
                    resource['difficulty_level'],
                    teacher_id
                )
            )
            count += 1
        except Exception as e:
            print(f"⚠️ Erreur lors de l'ajout de '{resource['title']}': {e}")
    
    return count

def create_test_data():
    """Crée des données de test pour l'application"""
    
    print("🔧 Initialisation de la base de données...")
    
    try:
        # Créer un enseignant
        print("\n👨‍🏫 Création d'un enseignant de test...")
        teacher_password = bcrypt.hashpw("teacher123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Vérifier si l'enseignant existe déjà
        check_query = "SELECT id FROM users WHERE email = %s"
        existing = Database.execute_query_one(check_query, ("enseignant@enspd.cm",))
        
        if existing:
            teacher_id = existing['id']
            print(f"ℹ️ Enseignant existe déjà (ID: {teacher_id})")
        else:
            query = """
                INSERT INTO users (email, password_hash, first_name, last_name, role)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (
                "enseignant@enspd.cm",
                teacher_password,
                "Marie",
                "Kouam",
                "teacher"
            ))
            result = cursor.fetchone()
            conn.commit()
            cursor.close()
            conn.close()
            
            teacher_id = result[0]
            print(f"✅ Enseignant créé (ID: {teacher_id})")
        
        # Créer des matières
        print("\n📚 Création des matières...")
        subjects_data = [
            ("Mathématiques", "MATH101", "Sciences", 6, teacher_id),
            ("Physique", "PHY101", "Sciences", 6, teacher_id),
            ("Programmation Python", "INFO101", "Informatique", 6, teacher_id),
            ("Algorithmique", "INFO102", "Informatique", 6, teacher_id),
            ("Base de données", "INFO103", "Informatique", 6, teacher_id),
            ("Réseaux", "INFO104", "Informatique", 4, teacher_id)
        ]
        
        for subject in subjects_data:
            query = """
                INSERT INTO subjects (name, code, department, credits, teacher_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (code) DO NOTHING
            """
            Database.execute_query(query, subject)
        
        print("✅ Matières créées")
        
        # Récupérer les IDs des matières
        subject_query = "SELECT id, code FROM subjects ORDER BY id LIMIT 6"
        subjects = Database.execute_query(subject_query, fetch=True)
        subject_ids = [dict(s)['id'] for s in subjects] if subjects else []
        
        # Créer des étudiants
        print("\n👨‍🎓 Création d'étudiants de test...")
        students = [
            ("etudiant1@enspd.cm", "student123", "Jean", "Mbarga", "ENSPD2024001", "Informatique", "L3"),
            ("etudiant2@enspd.cm", "student123", "Marie", "Ngo", "ENSPD2024002", "Informatique", "L3"),
            ("etudiant3@enspd.cm", "student123", "Paul", "Kamga", "ENSPD2024003", "Sciences", "L2")
        ]
        
        student_ids = []
        for email, password, first_name, last_name, student_id, dept, level in students:
            # Vérifier si l'étudiant existe déjà
            check_query = "SELECT id FROM users WHERE email = %s"
            existing = Database.execute_query_one(check_query, (email,))
            
            if existing:
                user_id = existing['id']
                print(f"ℹ️ Étudiant existe déjà: {first_name} {last_name} (ID: {user_id})")
            else:
                # Créer l'utilisateur
                user = User.create_user(email, password, first_name, last_name, "student")
                if user:
                    user_id = user['id']
                    # Créer le profil étudiant
                    User.create_student_profile(user_id, student_id, dept, level, "2024-2025")
                    print(f"✅ Étudiant créé: {first_name} {last_name} (ID: {user_id})")
            
            student_ids.append(user_id)
        
        # Créer des notes
        print("\n📊 Création de notes de test...")
        if len(student_ids) < 3:
            print("⚠️ Pas assez d'étudiants créés pour les notes")
            return
        
        if len(subject_ids) < 5:
            print("⚠️ Pas assez de matières créées pour les notes")
            return
            
        grades_data = [
            # Étudiant 1 - Bon étudiant
            (student_ids[0], subject_ids[0], "Examen", 15.5, "S1", "2024-2025"),
            (student_ids[0], subject_ids[1], "Examen", 14.0, "S1", "2024-2025"),
            (student_ids[0], subject_ids[2], "Examen", 17.5, "S1", "2024-2025"),
            (student_ids[0], subject_ids[3], "Examen", 16.0, "S1", "2024-2025"),
            (student_ids[0], subject_ids[4], "Examen", 15.0, "S1", "2024-2025"),
            # Étudiant 2 - Étudiant moyen
            (student_ids[1], subject_ids[0], "Examen", 11.5, "S1", "2024-2025"),
            (student_ids[1], subject_ids[1], "Examen", 10.0, "S1", "2024-2025"),
            (student_ids[1], subject_ids[2], "Examen", 12.5, "S1", "2024-2025"),
            (student_ids[1], subject_ids[3], "Examen", 11.0, "S1", "2024-2025"),
            # Étudiant 3 - Étudiant en difficulté
            (student_ids[2], subject_ids[0], "Examen", 7.5, "S1", "2024-2025"),
            (student_ids[2], subject_ids[1], "Examen", 8.0, "S1", "2024-2025"),
            (student_ids[2], subject_ids[2], "Examen", 6.5, "S1", "2024-2025"),
            (student_ids[2], subject_ids[3], "Examen", 9.0, "S1", "2024-2025")
        ]
        
        for grade in grades_data:
            query = """
                INSERT INTO grades (student_id, subject_id, grade_type, score, semester, academic_year)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """
            Database.execute_query(query, grade)
        
        print("✅ Notes créées")
        
        # Créer des ressources pédagogiques complètes
        print("\n📚 Création de ressources pédagogiques...")
        resources_count = create_educational_resources(teacher_id)
        print(f"✅ {resources_count} ressources créées")
        
        print("\n" + "=" * 50)
        print("✅ Initialisation terminée avec succès!")
        print("\n📝 Comptes de test créés:")
        print("   Enseignant: enseignant@enspd.cm / teacher123")
        print("   Étudiant 1: etudiant1@enspd.cm / student123 (Bon étudiant)")
        print("   Étudiant 2: etudiant2@enspd.cm / student123 (Étudiant moyen)")
        print("   Étudiant 3: etudiant3@enspd.cm / student123 (Étudiant en difficulté)")
        print(f"\n📚 Ressources pédagogiques: {resources_count} ressources créées")
        print("   - 7 ressources par matière (débutant, intermédiaire, avancé)")
        print("   - 4 ressources générales (méthodes de travail, etc.)")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_test_data()
