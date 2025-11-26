"""
Test du service Groq
"""
from services.groq_service import GroqService
from config import Config

def test_groq():
    print("🧪 Test du service Groq...\n")
    
    # Vérifier la clé API
    if Config.GROQ_API_KEY:
        print(f"✅ GROQ_API_KEY configurée: {Config.GROQ_API_KEY[:20]}...")
    else:
        print("❌ GROQ_API_KEY non configurée!")
        return
    
    # Initialiser le service
    groq = GroqService()
    
    if not groq.client:
        print("❌ Client Groq non initialisé!")
        return
    
    # Tester une requête simple
    print("\n📝 Test de génération de réponse...")
    response = groq.generate_chatbot_response(
        "Bonjour, comment puis-je améliorer mes notes en mathématiques?",
        context="Étudiant en L1, moyenne actuelle: 12/20"
    )
    
    if response:
        print(f"\n✅ Réponse générée:\n{response}")
    else:
        print("\n❌ Aucune réponse générée!")

if __name__ == "__main__":
    test_groq()
