# Service pour l'intégration de l'API Groq
from groq import Groq
from config import Config

class GroqService:
    """Service pour interagir avec l'API Groq"""
    
    def __init__(self):
        """Initialise le service Groq"""
        try:
            self.client = Groq(api_key=Config.GROQ_API_KEY)
            # Utiliser un modèle actif (llama-3.1-70b-versatile est décommissionné)
            self.model = "llama-3.3-70b-versatile"  # Nouveau modèle recommandé
            print(f"✅ Groq initialisé avec {self.model}")
        except Exception as e:
            print(f"❌ Erreur initialisation Groq: {e}")
            self.client = None
    
    def generate_chatbot_response(self, user_message, context=None, conversation_history=None):
        """Génère une réponse du chatbot éducatif avec historique conversationnel"""
        if self.client is None:
            return None
        
        # Prompt système pour le chatbot éducatif
        system_prompt = """Tu es un assistant éducatif intelligent pour l'École Normale Supérieure Polytechnique de Douala (ENSPD).
        
        Ton rôle:
        - Aider les étudiants avec leurs questions académiques
        - Expliquer des concepts complexes de manière simple
        - Recommander des stratégies d'apprentissage
        - Motiver et encourager les étudiants
        - Répondre en français de manière claire et pédagogique
        - Te souvenir du contexte de la conversation pour des réponses cohérentes
        
        Domaines d'expertise:
        - Mathématiques, Physique, Informatique, Génie
        - Méthodologie d'apprentissage
        - Gestion du temps et organisation
        - Préparation aux examens
        
        Sois toujours positif, encourageant et précis dans tes réponses.
        Limite tes réponses à 300 mots maximum pour rester concis."""
        
        # Construire les messages avec historique
        messages = [{"role": "system", "content": system_prompt}]
        
        if context:
            messages.append({
                "role": "system",
                "content": f"Contexte de l'étudiant: {context}"
            })
        
        # Ajouter l'historique de conversation (5 derniers échanges)
        if conversation_history:
            messages.extend(conversation_history)
        
        # Ajouter le message actuel
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                top_p=1,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ Erreur Groq API: {e}")
            return None
    
    def analyze_performance(self, student_data):
        """Analyse les performances d'un étudiant avec Groq"""
        prompt = f"""Analyse les performances académiques suivantes d'un étudiant de l'ENSPD:
        
        {student_data}
        
        Fournis en français:
        1. Une analyse des points forts
        2. Les domaines à améliorer
        3. Des recommandations concrètes
        4. Des conseils motivants
        
        Sois concis (maximum 250 mots)."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=400
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ Erreur Groq API: {e}")
            return "Analyse non disponible pour le moment."
