# Service pour l'intégration de l'API Gemini
import google.generativeai as genai
from config import Config

class GeminiService:
    """Service pour interagir avec l'API Gemini"""
    
    def __init__(self):
        """Initialise le service Gemini (avec Groq en priorité)"""
        # Essayer Groq en premier
        try:
            from services.groq_service import GroqService
            self.groq = GroqService()
            if self.groq.client:
                print("✅ Chatbot initialisé avec Groq (IA complète activée)")
                self.use_groq = True
                return
        except Exception as e:
            print(f"⚠️ Groq non disponible: {e}")
        
        # Fallback sur le mode sans API
        self.use_groq = False
        self.groq = None
        print("✅ Chatbot initialisé en mode fallback (réponses intelligentes activées)")
    
    def generate_chatbot_response(self, user_message, context=None, conversation_history=None):
        """Génère une réponse du chatbot éducatif avec historique"""
        # Prompt système pour le chatbot éducatif
        system_prompt = """
        Tu es un assistant éducatif intelligent pour l'École Normale Supérieure Polytechnique de Douala (ENSPD).
        
        Ton rôle:
        - Aider les étudiants avec leurs questions académiques
        - Expliquer des concepts complexes de manière simple
        - Recommander des stratégies d'apprentissage
        - Motiver et encourager les étudiants
        - Répondre en français de manière claire et pédagogique
        
        Domaines d'expertise:
        - Mathématiques, Physique, Informatique, Génie
        - Méthodologie d'apprentissage
        - Gestion du temps et organisation
        - Préparation aux examens
        
        Sois toujours positif, encourageant et précis dans tes réponses.
        """
        
        # Ajouter le contexte si disponible
        full_prompt = system_prompt + "\n\n"
        if context:
            full_prompt += f"Contexte de l'étudiant: {context}\n\n"
        full_prompt += f"Question de l'étudiant: {user_message}\n\nRéponse:"
        
        # Essayer Groq en premier (avec historique)
        if hasattr(self, 'use_groq') and self.use_groq and self.groq:
            try:
                response = self.groq.generate_chatbot_response(user_message, context, conversation_history)
                if response:
                    return response
            except Exception as e:
                print(f"⚠️ Erreur Groq: {e}")
        
        # Fallback sur les réponses pré-programmées
        return self._get_fallback_response(user_message, context)
    
    def _get_fallback_response(self, user_message, context=None):
        """Génère une réponse de secours si l'API Gemini ne fonctionne pas"""
        message_lower = user_message.lower()
        
        # Réponses basées sur des mots-clés
        if any(word in message_lower for word in ['bonjour', 'salut', 'hello', 'hi', 'bonsoir']):
            return "Bonjour ! Je suis votre assistant éducatif. Comment puis-je vous aider avec vos études aujourd'hui ?"
        
        elif any(word in message_lower for word in ['comment', 'ça va', 'tu vas', 'vas-tu']):
            return "Je vais bien, merci ! Je suis là pour vous aider avec vos études. Avez-vous des questions sur vos cours, vos notes, ou besoin de conseils pour mieux apprendre ?"
        
        elif any(word in message_lower for word in ['aide', 'aider', 'help']):
            return """Je peux vous aider avec :
            
📚 Vos questions académiques (mathématiques, physique, informatique, etc.)
📖 Des conseils de méthodologie d'apprentissage
⏰ L'organisation et la gestion du temps
📝 La préparation aux examens
💡 Des recommandations de ressources

Posez-moi une question spécifique et je ferai de mon mieux pour vous aider !"""
        
        elif any(word in message_lower for word in ['math', 'mathématique', 'calcul']):
            return """Pour les mathématiques, je vous recommande :

✅ Pratiquer régulièrement avec des exercices
✅ Comprendre les concepts avant de mémoriser les formules
✅ Faire des fiches de révision
✅ Travailler en groupe pour échanger
✅ Consulter les ressources recommandées dans votre dashboard

Quelle partie des mathématiques vous pose problème ?"""
        
        elif any(word in message_lower for word in ['examen', 'test', 'contrôle']):
            return """Conseils pour bien préparer vos examens :

📅 Commencez vos révisions au moins 2 semaines avant
📝 Faites des fiches de synthèse
🔄 Révisez par sessions de 45 minutes avec des pauses
👥 Formez des groupes d'étude
📊 Faites des exercices d'annales
😴 Dormez bien la veille de l'examen
🧘 Gérez votre stress avec des techniques de relaxation

Besoin de conseils plus spécifiques ?"""
        
        elif any(word in message_lower for word in ['note', 'moyenne', 'résultat']):
            return """Pour améliorer vos notes :

1️⃣ Identifiez vos points faibles (consultez vos statistiques)
2️⃣ Travaillez régulièrement, pas seulement avant les examens
3️⃣ Utilisez les ressources recommandées pour vos matières faibles
4️⃣ Participez activement en cours
5️⃣ Faites tous les exercices proposés
6️⃣ N'hésitez pas à demander de l'aide à vos enseignants

Consultez la page "Recommandations" pour des ressources adaptées à votre niveau !"""
        
        elif any(word in message_lower for word in ['motivation', 'motivé', 'découragé']):
            return """💪 Gardez votre motivation !

✨ Rappelez-vous pourquoi vous avez choisi ces études
🎯 Fixez-vous des objectifs réalisables
🏆 Célébrez vos petites victoires
👥 Entourez-vous de personnes positives
📈 Suivez vos progrès dans votre dashboard
💡 Chaque difficulté est une opportunité d'apprendre

Vous êtes capable de réussir ! Continuez vos efforts ! 🚀"""
        
        else:
            return f"""Merci pour votre question ! 

⚠️ Le service IA est temporairement indisponible, mais je peux quand même vous aider :

📚 Consultez la page "Recommandations" pour des ressources adaptées à vos matières faibles
📊 Vérifiez vos statistiques dans le dashboard
📖 Explorez les ressources pédagogiques disponibles

Pour une question spécifique sur : mathématiques, examens, motivation, ou organisation, reformulez votre question avec ces mots-clés.

Votre question : "{user_message}"

Je ferai de mon mieux pour vous répondre avec les informations disponibles !"""
    
    def analyze_performance(self, student_data):
        """Analyse les performances d'un étudiant avec Groq ou fallback"""
        # Essayer Groq
        if hasattr(self, 'use_groq') and self.use_groq and self.groq:
            try:
                return self.groq.analyze_performance(student_data)
            except Exception as e:
                print(f"⚠️ Erreur Groq: {e}")
        
        # Fallback
        return "Analyse non disponible pour le moment."
    
    def generate_study_recommendations(self, subject, difficulty_level, student_profile):
        """Génère des recommandations d'étude personnalisées"""
        prompt = f"""
        Génère des recommandations d'étude pour un étudiant de l'ENSPD:
        
        Matière: {subject}
        Niveau de difficulté: {difficulty_level}
        Profil: {student_profile}
        
        Recommande:
        1. Des ressources d'apprentissage spécifiques
        2. Une méthodologie adaptée
        3. Un planning de révision
        4. Des exercices pratiques
        
        Réponds en français de manière pratique et actionnable.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Erreur Gemini API: {e}")
            return "Recommandations non disponibles pour le moment."
