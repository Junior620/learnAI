# Script pour ajouter plus de notes aux étudiants existants
import sys
import os
import random

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import Database

def add_grades_to_students(num_grades_per_student=100):
    """Ajoute des notes supplémentaires à tous les étudiants"""
    
    print("=" * 70)
    print(f"Ajout de {num_grades_per_student} notes par étudiant")
    print("=" * 70)
    
    try:
        # Récupérer tous les étudiants
        query_students = """
            SELECT u.id, sp.student_id, u.first_name, u.last_name
            FROM users u
            LEFT JOIN student_profiles sp ON u.id = sp.user_id
            WHERE u.role = 'student'
        """
        students = Database.execute_query(query_students, fetch=True)
        
        if not students:
            print("❌ Aucun étudiant trouvé")
            return False
        
        print(f"✅ {len(students)} étudiants trouvés")
        
        # Récupérer les matières
        query_subjects = "SELECT id FROM subjects"
        subjects = Database.execute_query(query_subjects, fetch=True)
        
        if not subjects or len(subjects) < 4:
            print("❌ Pas assez de matières")
            return False
        
        subject_ids = [dict(s)['id'] for s in subjects]
        print(f"✅ {len(subject_ids)} matières trouvées")
        
        # Récupérer la moyenne actuelle de chaque étudiant pour garder la cohérence
        print("\n📊 Calcul des profils étudiants...")
        
        conn = Database.get_connection()
        cursor = conn.cursor()
        
        total_grades_added = 0
        students_processed = 0
        
        for student in students:
            student_id = dict(student)['id']
            
            # Récupérer la moyenne actuelle
            query_avg = """
                SELECT AVG(score) as avg_score, STDDEV(score) as std_score
                FROM grades
                WHERE student_id = %s
            """
            cursor.execute(query_avg, (student_id,))
            avg_data = cursor.fetchone()
            
            if avg_data and avg_data[0]:
                current_avg = float(avg_data[0])
                current_std = float(avg_data[1]) if avg_data[1] else 1.5
            else:
                # Si pas de notes, générer un profil aléatoire
                profiles = [
                    (15, 2.0),   # Excellent
                    (13, 1.5),   # Bon
                    (11, 1.8),   # Moyen
                    (9, 2.0),    # Faible
                    (7, 1.5)     # Très faible
                ]
                current_avg, current_std = random.choice(profiles)
            
            # Générer les notes autour de cette moyenne
            grades_to_add = []
            
            # Types d'évaluation variés
            grade_types = ['Examen', 'TP', 'Contrôle', 'Devoir', 'Projet', 'Quiz']
            semesters = ['S1', 'S2']
            years = ['2023-2024', '2024-2025']
            
            for _ in range(num_grades_per_student):
                # Générer une note cohérente avec le profil
                score = random.gauss(current_avg, current_std)
                score = max(0, min(20, score))  # Entre 0 et 20
                score = round(score * 2) / 2  # Arrondir à 0.5
                
                subject_id = random.choice(subject_ids)
                grade_type = random.choice(grade_types)
                semester = random.choice(semesters)
                year = random.choice(years)
                
                grades_to_add.append((student_id, subject_id, grade_type, score, semester, year))
            
            # Insérer toutes les notes en batch
            query_insert = """
                INSERT INTO grades (student_id, subject_id, grade_type, score, semester, academic_year)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            try:
                cursor.executemany(query_insert, grades_to_add)
                total_grades_added += len(grades_to_add)
                students_processed += 1
                
                # Commit tous les 100 étudiants
                if students_processed % 100 == 0:
                    conn.commit()
                    print(f"  ✓ {students_processed}/{len(students)} étudiants traités...")
            
            except Exception as e:
                print(f"  ⚠️ Erreur pour étudiant {student_id}: {e}")
                conn.rollback()
                continue
        
        # Commit final
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 70)
        print("✅ Ajout de notes terminé avec succès!")
        print(f"   📊 Étudiants traités: {students_processed}")
        print(f"   📝 Notes ajoutées: {total_grades_added:,}")
        print(f"   📈 Moyenne par étudiant: {total_grades_added / students_processed:.1f}")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Ajouter des notes aux étudiants')
    parser.add_argument('--grades', type=int, default=100, 
                       help='Nombre de notes à ajouter par étudiant (défaut: 100)')
    
    args = parser.parse_args()
    
    print("\n🎓 ENSPD LearnAI - Ajout de Notes")
    print(f"Nombre de notes par étudiant: {args.grades}\n")
    
    success = add_grades_to_students(args.grades)
    
    if success:
        print("\n🚀 Vous pouvez maintenant:")
        print("   1. Réentraîner le modèle ML: python ml/train_model.py")
        print("   2. Tester l'application avec des données enrichies")
    else:
        print("\n❌ L'ajout de notes a échoué.")
