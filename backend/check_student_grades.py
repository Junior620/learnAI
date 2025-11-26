"""
Vérifier les notes d'un étudiant
"""
from models.database import Database

def check_student_grades():
    print("📊 Vérification des notes...\n")
    
    # ID de l'étudiant etudiant1@enspd.cm
    student_id = 5
    
    # Compter les notes
    query = "SELECT COUNT(*) as count FROM grades WHERE student_id = %s"
    result = Database.execute_query_one(query, (student_id,))
    print(f"📈 Total notes pour student_id {student_id}: {result['count']}")
    
    # Lister quelques notes
    query = """
        SELECT g.*, s.name as subject_name
        FROM grades g
        JOIN subjects s ON g.subject_id = s.id
        WHERE g.student_id = %s
        LIMIT 10
    """
    grades = Database.execute_query(query, (student_id,), fetch=True)
    
    if grades:
        print("\n📋 Quelques notes:")
        for grade in grades:
            print(f"   {grade['subject_name']}: {grade['score']}/20 ({grade['grade_type']}, {grade['semester']})")
    else:
        print("\n❌ Aucune note trouvée!")
        
        # Vérifier s'il y a des notes dans la base
        query = "SELECT COUNT(*) as count FROM grades"
        result = Database.execute_query_one(query)
        print(f"\n📊 Total notes dans la base: {result['count']}")
        
        # Lister les student_id qui ont des notes
        query = """
            SELECT DISTINCT student_id, COUNT(*) as count
            FROM grades
            GROUP BY student_id
            ORDER BY student_id
            LIMIT 10
        """
        students = Database.execute_query(query, fetch=True)
        print("\n👥 Étudiants avec des notes:")
        for student in students:
            print(f"   Student ID {student['student_id']}: {student['count']} notes")

if __name__ == "__main__":
    check_student_grades()
