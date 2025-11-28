# Routes pour le chatbot Gemini
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.gemini_service import GeminiService
from models.database import Database

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

def get_student_detailed_data(user_id):
    """Récupère toutes les données détaillées de l'étudiant"""
    # Informations de base
    base_query = """
        SELECT 
            u.first_name,
            u.last_name,
            u.email,
            sp.department,
            sp.level,
            sp.student_id,
            AVG(g.score) as avg_score
        FROM users u
        LEFT JOIN student_profiles sp ON u.id = sp.user_id
        LEFT JOIN grades g ON u.id = g.student_id
        WHERE u.id = %s
        GROUP BY u.first_name, u.last_name, u.email, sp.department, sp.level, sp.student_id
    """
    base_data = Database.execute_query_one(base_query, (user_id,))
    
    # Notes par matière
    grades_query = """
        SELECT 
            s.name as subject_name,
            g.score,
            g.coefficient,
            g.exam_date,
            g.exam_type
        FROM grades g
        JOIN subjects s ON g.subject_id = s.id
        WHERE g.student_id = %s
        ORDER BY g.exam_date DESC
    """
    grades_data = Database.execute_query(grades_query, (user_id,), fetch=True)
    
    # Moyennes par matière
    subject_avg_query = """
        SELECT 
            s.name as subject_name,
            AVG(g.score) as avg_score,
            COUNT(*) as num_grades
        FROM grades g
        JOIN subjects s ON g.subject_id = s.id
        WHERE g.student_id = %s
        GROUP BY s.name
        ORDER BY avg_score DESC
    """
    subject_avgs = Database.execute_query(subject_avg_query, (user_id,), fetch=True)
    
    return {
        'base': base_data,
        'grades': list(grades_data) if grades_data else [],
        'subject_averages': list(subject_avgs) if subject_avgs else []
    }

@chatbot_bp.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    """Envoie un message au chatbot et reçoit une réponse avec historique"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('message'):
        return jsonify({"error": "Message requis"}), 400
    
    user_message = data['message']
    
    try:
        # Récupérer les données détaillées de l'étudiant
        student_data = get_student_detailed_data(user_id)
        
        # Construire un contexte enrichi
        context = None
        context_json = None
        
        if student_data['base']:
            base = student_data['base']
            avg_score = base.get('avg_score')
            avg_str = f"{float(avg_score):.2f}" if avg_score else "N/A"
            
            # Contexte textuel pour l'IA
            context_parts = [
                f"Étudiant: {base['first_name']} {base['last_name']}",
                f"Matricule: {base.get('student_id', 'N/A')}",
                f"Département: {base.get('department', 'N/A')}",
                f"Niveau: {base.get('level', 'N/A')}",
                f"Moyenne générale: {avg_str}/20"
            ]
            
            # Ajouter les moyennes par matière
            if student_data['subject_averages']:
                context_parts.append("\nMoyennes par matière:")
                for subj in student_data['subject_averages']:
                    context_parts.append(f"- {subj['subject_name']}: {float(subj['avg_score']):.2f}/20 ({subj['num_grades']} notes)")
            
            # Ajouter les dernières notes
            if student_data['grades']:
                context_parts.append("\nDernières notes:")
                for grade in student_data['grades'][:5]:  # 5 dernières notes
                    context_parts.append(f"- {grade['subject_name']}: {grade['score']}/20 (coef {grade['coefficient']})")
            
            context = "\n".join(context_parts)
            
            # JSON pour la base de données
            context_json = {
                "first_name": base['first_name'],
                "last_name": base['last_name'],
                "department": base.get('department'),
                "level": base.get('level'),
                "avg_score": avg_str,
                "subject_count": len(student_data['subject_averages']),
                "total_grades": len(student_data['grades'])
            }
        
        # Récupérer l'historique récent (5 derniers messages)
        history_query = """
            SELECT message, response
            FROM chatbot_conversations
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 5
        """
        history_data = Database.execute_query(history_query, (user_id,), fetch=True)
        conversation_history = []
        
        if history_data:
            # Inverser pour avoir l'ordre chronologique
            for h in reversed(list(history_data)):
                conversation_history.append({
                    "role": "user",
                    "content": h['message']
                })
                conversation_history.append({
                    "role": "assistant",
                    "content": h['response']
                })
        
        # Générer la réponse avec Gemini (avec historique et données complètes)
        gemini = GeminiService()
        response = gemini.generate_chatbot_response(user_message, context, conversation_history, student_data)
        
        # Sauvegarder la conversation
        try:
            import json
            
            # Convertir le contexte en JSON string pour PostgreSQL JSONB
            context_str = json.dumps(context_json) if context_json else None
            
            # Debug
            print(f"💾 Sauvegarde conversation - Context JSON: {context_str}")
            
            # Essayer d'abord avec le contexte JSON
            try:
                save_query = """
                    INSERT INTO chatbot_conversations (user_id, message, response, context)
                    VALUES (%s, %s, %s, %s::jsonb)
                """
                Database.execute_query(save_query, (user_id, user_message, response, context_str))
                print("✅ Conversation sauvegardée avec contexte JSON")
            except Exception as json_error:
                # Si ça échoue, sauvegarder sans contexte
                print(f"⚠️ Erreur avec contexte JSON: {json_error}")
                print("🔄 Tentative de sauvegarde sans contexte...")
                save_query_simple = """
                    INSERT INTO chatbot_conversations (user_id, message, response)
                    VALUES (%s, %s, %s)
                """
                Database.execute_query(save_query_simple, (user_id, user_message, response))
                print("✅ Conversation sauvegardée sans contexte")
                
        except Exception as save_error:
            print(f"❌ Erreur sauvegarde conversation: {save_error}")
            # Continue même si la sauvegarde échoue
        
        return jsonify({
            "message": user_message,
            "response": response
        }), 200
        
    except Exception as e:
        print(f"❌ Erreur dans send_message: {e}")
        import traceback
        traceback.print_exc()
        
        # Retourner une réponse de secours
        return jsonify({
            "message": user_message,
            "response": "Je suis désolé, je rencontre un problème technique. Veuillez réessayer dans quelques instants. En attendant, consultez la page 'Recommandations' pour des ressources adaptées à vos besoins."
        }), 200

@chatbot_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    """Récupère l'historique des conversations"""
    user_id = get_jwt_identity()
    
    query = """
        SELECT message, response, created_at
        FROM chatbot_conversations
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 50
    """
    history = Database.execute_query(query, (user_id,), fetch=True)
    
    return jsonify({
        "history": [dict(h) for h in history] if history else []
    }), 200
