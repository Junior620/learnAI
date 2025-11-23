# Routes pour le chatbot Gemini
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.gemini_service import GeminiService
from models.database import Database

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

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
        # Récupérer le contexte de l'étudiant
        query = """
            SELECT 
                u.first_name,
                sp.department,
                sp.level,
                AVG(g.score) as avg_score
            FROM users u
            LEFT JOIN student_profiles sp ON u.id = sp.user_id
            LEFT JOIN grades g ON u.id = g.student_id
            WHERE u.id = %s
            GROUP BY u.first_name, sp.department, sp.level
        """
        context_data = Database.execute_query_one(query, (user_id,))
        
        context = None
        context_json = None
        if context_data:
            avg_score = context_data.get('avg_score')
            avg_str = f"{float(avg_score):.2f}" if avg_score else "N/A"
            context = f"Étudiant: {context_data['first_name']}, Département: {context_data.get('department', 'N/A')}, Niveau: {context_data.get('level', 'N/A')}, Moyenne: {avg_str}"
            
            # Créer un objet JSON pour la base de données
            context_json = {
                "first_name": context_data['first_name'],
                "department": context_data.get('department'),
                "level": context_data.get('level'),
                "avg_score": avg_str
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
        
        # Générer la réponse avec Gemini (avec historique)
        gemini = GeminiService()
        response = gemini.generate_chatbot_response(user_message, context, conversation_history)
        
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
