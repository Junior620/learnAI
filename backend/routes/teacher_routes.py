# Routes pour les enseignants
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.database import Database
from models.user import User

teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')

@teacher_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """Récupère les données du tableau de bord enseignant"""
    user_id = get_jwt_identity()
    
    # Statistiques globales
    query_stats = """
        SELECT 
            COUNT(DISTINCT g.student_id) as total_students,
            COALESCE(AVG(g.score), 0) as class_average,
            COUNT(*) as total_grades
        FROM grades g
        JOIN subjects s ON g.subject_id = s.id
        WHERE s.teacher_id = %s
    """
    stats = Database.execute_query_one(query_stats, (user_id,))
    
    # Étudiants en difficulté
    query_struggling = """
        SELECT 
            u.id,
            u.first_name,
            u.last_name,
            sp.student_id,
            AVG(g.score) as avg_score
        FROM users u
        JOIN student_profiles sp ON u.id = sp.user_id
        JOIN grades g ON u.id = g.student_id
        JOIN subjects s ON g.subject_id = s.id
        WHERE s.teacher_id = %s
        GROUP BY u.id, u.first_name, u.last_name, sp.student_id
        HAVING AVG(g.score) < 10
        ORDER BY avg_score ASC
    """
    struggling = Database.execute_query(query_struggling, (user_id,), fetch=True)
    
    # Formater les statistiques
    statistics = {
        'total_students': stats['total_students'] if stats else 0,
        'class_average': float(stats['class_average']) if stats and stats['class_average'] else 0,
        'total_grades': stats['total_grades'] if stats else 0
    }
    
    return jsonify({
        "statistics": statistics,
        "struggling_students": [dict(s) for s in struggling] if struggling else []
    }), 200

@teacher_bp.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    """Récupère la liste de tous les étudiants avec leurs moyennes"""
    query = """
        SELECT 
            u.id, u.email, u.first_name, u.last_name,
            sp.student_id, sp.department, sp.level,
            COALESCE(AVG(g.score), 0) as avg_score
        FROM users u
        LEFT JOIN student_profiles sp ON u.id = sp.user_id
        LEFT JOIN grades g ON u.id = g.student_id
        WHERE u.role = 'student'
        GROUP BY u.id, u.email, u.first_name, u.last_name, sp.student_id, sp.department, sp.level
        ORDER BY u.last_name, u.first_name
    """
    students = Database.execute_query(query, fetch=True)
    return jsonify({"students": [dict(s) for s in students] if students else []}), 200

@teacher_bp.route('/student/<int:student_id>/performance', methods=['GET'])
@jwt_required()
def get_student_performance(student_id):
    """Récupère les performances détaillées d'un étudiant"""
    
    # Récupérer les infos de l'étudiant
    student_query = """
        SELECT 
            u.id, u.email, u.first_name, u.last_name,
            sp.student_id, sp.department, sp.level, sp.academic_year
        FROM users u
        LEFT JOIN student_profiles sp ON u.id = sp.user_id
        WHERE u.id = %s
    """
    student = Database.execute_query_one(student_query, (student_id,))
    
    if not student:
        return jsonify({"error": "Étudiant non trouvé"}), 404
    
    # Récupérer toutes les notes
    grades_query = """
        SELECT 
            g.id, g.score, g.grade_type, g.semester, g.academic_year, g.created_at,
            s.name as subject_name, s.code as subject_code
        FROM grades g
        JOIN subjects s ON g.subject_id = s.id
        WHERE g.student_id = %s
        ORDER BY g.created_at DESC
    """
    grades = Database.execute_query(grades_query, (student_id,), fetch=True)
    
    # Calculer les statistiques
    stats_query = """
        SELECT 
            AVG(score) as average_score,
            COUNT(*) as total_grades,
            COUNT(DISTINCT subject_id) as subjects_count
        FROM grades
        WHERE student_id = %s
    """
    stats = Database.execute_query_one(stats_query, (student_id,))
    
    return jsonify({
        "student": dict(student),
        "grades": [dict(g) for g in grades] if grades else [],
        "statistics": dict(stats) if stats else {}
    }), 200

@teacher_bp.route('/subjects', methods=['GET'])
@jwt_required()
def get_subjects():
    """Récupère la liste des matières"""
    query = "SELECT id, name, code FROM subjects ORDER BY name"
    subjects = Database.execute_query(query, fetch=True)
    
    return jsonify({
        "subjects": [dict(s) for s in subjects] if subjects else []
    }), 200

@teacher_bp.route('/grade', methods=['POST'])
@jwt_required()
def add_grade():
    """Ajoute une note pour un étudiant"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validation
    required_fields = ['student_id', 'subject_id', 'score', 'grade_type', 'semester']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Champ requis: {field}"}), 400
    
    # Vérifier que la note est entre 0 et 20
    score = float(data['score'])
    if score < 0 or score > 20:
        return jsonify({"error": "La note doit être entre 0 et 20"}), 400
    
    # Insérer la note
    query = """
        INSERT INTO grades (student_id, subject_id, grade_type, score, semester, academic_year)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """
    
    try:
        result = Database.execute_query_one(
            query,
            (
                data['student_id'],
                data['subject_id'],
                data['grade_type'],
                score,
                data['semester'],
                data.get('academic_year', '2024-2025')
            )
        )
        
        return jsonify({
            "message": "Note ajoutée avec succès",
            "grade_id": result['id'] if result else None
        }), 201
    except Exception as e:
        print(f"Erreur ajout note: {e}")
        return jsonify({"error": "Erreur lors de l'ajout de la note"}), 500

@teacher_bp.route('/grade/<int:grade_id>', methods=['PUT'])
@jwt_required()
def update_grade(grade_id):
    """Modifie une note existante"""
    data = request.get_json()
    
    if 'score' not in data:
        return jsonify({"error": "Score requis"}), 400
    
    score = float(data['score'])
    if score < 0 or score > 20:
        return jsonify({"error": "La note doit être entre 0 et 20"}), 400
    
    query = "UPDATE grades SET score = %s WHERE id = %s"
    
    try:
        Database.execute_query(query, (score, grade_id))
        return jsonify({"message": "Note modifiée avec succès"}), 200
    except Exception as e:
        print(f"Erreur modification note: {e}")
        return jsonify({"error": "Erreur lors de la modification"}), 500

@teacher_bp.route('/grade/<int:grade_id>', methods=['DELETE'])
@jwt_required()
def delete_grade(grade_id):
    """Supprime une note"""
    query = "DELETE FROM grades WHERE id = %s"
    
    try:
        Database.execute_query(query, (grade_id,))
        return jsonify({"message": "Note supprimée avec succès"}), 200
    except Exception as e:
        print(f"Erreur suppression note: {e}")
        return jsonify({"error": "Erreur lors de la suppression"}), 500
