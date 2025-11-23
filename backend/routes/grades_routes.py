# Routes pour la gestion des notes
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.database import Database

grades_bp = Blueprint('grades', __name__, url_prefix='/api/grades')

@grades_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_grades():
    """Récupère toutes les notes de l'étudiant avec statistiques détaillées"""
    user_id = get_jwt_identity()
    
    # Récupérer toutes les notes
    query_grades = """
        SELECT g.*, s.name as subject_name, s.code as subject_code
        FROM grades g
        JOIN subjects s ON g.subject_id = s.id
        WHERE g.student_id = %s
        ORDER BY g.created_at DESC
    """
    grades = Database.execute_query(query_grades, (user_id,), fetch=True)
    
    # Statistiques globales
    query_stats = """
        SELECT 
            AVG(score) as avg_score,
            MIN(score) as min_score,
            MAX(score) as max_score,
            COUNT(*) as total_grades,
            COUNT(DISTINCT subject_id) as total_subjects
        FROM grades
        WHERE student_id = %s
    """
    stats = Database.execute_query_one(query_stats, (user_id,))
    
    # Statistiques par semestre
    query_semester = """
        SELECT 
            semester,
            AVG(score) as avg_score,
            COUNT(*) as total_grades
        FROM grades
        WHERE student_id = %s
        GROUP BY semester
        ORDER BY semester
    """
    semester_stats = Database.execute_query(query_semester, (user_id,), fetch=True)
    
    # Statistiques par matière
    query_subject = """
        SELECT 
            s.name as subject_name,
            AVG(g.score) as avg_score,
            MIN(g.score) as min_score,
            MAX(g.score) as max_score,
            COUNT(*) as total_grades
        FROM grades g
        JOIN subjects s ON g.subject_id = s.id
        WHERE g.student_id = %s
        GROUP BY s.id, s.name
        ORDER BY avg_score DESC
    """
    subject_stats = Database.execute_query(query_subject, (user_id,), fetch=True)
    
    return jsonify({
        "grades": [dict(g) for g in grades] if grades else [],
        "statistics": dict(stats) if stats else {},
        "semester_statistics": [dict(s) for s in semester_stats] if semester_stats else [],
        "subject_statistics": [dict(s) for s in subject_stats] if subject_stats else []
    }), 200

@grades_bp.route('/by-subject/<int:subject_id>', methods=['GET'])
@jwt_required()
def get_grades_by_subject(subject_id):
    """Récupère les notes d'une matière spécifique"""
    user_id = get_jwt_identity()
    
    query = """
        SELECT g.*, s.name as subject_name
        FROM grades g
        JOIN subjects s ON g.subject_id = s.id
        WHERE g.student_id = %s AND g.subject_id = %s
        ORDER BY g.created_at DESC
    """
    grades = Database.execute_query(query, (user_id, subject_id), fetch=True)
    
    return jsonify({
        "grades": [dict(g) for g in grades] if grades else []
    }), 200

@grades_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_detailed_statistics():
    """Récupère des statistiques détaillées sur les notes"""
    user_id = get_jwt_identity()
    
    # Distribution des notes
    query_distribution = """
        SELECT 
            CASE 
                WHEN score >= 16 THEN 'Excellent (16-20)'
                WHEN score >= 14 THEN 'Très bien (14-16)'
                WHEN score >= 12 THEN 'Bien (12-14)'
                WHEN score >= 10 THEN 'Passable (10-12)'
                ELSE 'Insuffisant (<10)'
            END as category,
            COUNT(*) as count
        FROM grades
        WHERE student_id = %s
        GROUP BY category
        ORDER BY MIN(score) DESC
    """
    distribution = Database.execute_query(query_distribution, (user_id,), fetch=True)
    
    # Évolution temporelle
    query_evolution = """
        SELECT 
            DATE_TRUNC('month', created_at) as month,
            AVG(score) as avg_score,
            COUNT(*) as total_grades
        FROM grades
        WHERE student_id = %s
        GROUP BY month
        ORDER BY month
    """
    evolution = Database.execute_query(query_evolution, (user_id,), fetch=True)
    
    return jsonify({
        "distribution": [dict(d) for d in distribution] if distribution else [],
        "evolution": [dict(e) for e in evolution] if evolution else []
    }), 200
