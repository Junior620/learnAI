#!/usr/bin/env python3
"""
Script pour tester l'API Gemini et lister les modèles disponibles
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import google.generativeai as genai
from config import Config

def test_gemini():
    """Teste l'API Gemini et liste les modèles disponibles"""
    
    print("🔧 Test de l'API Gemini...")
    print(f"✅ Clé API: {Config.GEMINI_API_KEY[:10]}...")
    
    print("\n" + "=" * 60)
    print("🧪 Test avec la NOUVELLE syntaxe (Client)")
    print("=" * 60)
    
    # Modèles à tester avec la nouvelle syntaxe
    new_models = [
        'gemini-2.5-flash',      # Le plus récent
        'gemini-2.0-flash-exp',
        'gemini-1.5-flash',
        'gemini-1.5-pro',
    ]
    
    for model_name in new_models:
        print(f"\n🔍 Test de '{model_name}' avec Client()...")
        try:
            from google import genai as new_genai
            client = new_genai.Client(api_key=Config.GEMINI_API_KEY)
            response = client.models.generate_content(
                model=model_name,
                contents="Dis bonjour en français"
            )
            print(f"   ✅ FONCTIONNE ! Réponse: {response.text[:50]}...")
            print(f"   👉 Utilisez ce modèle: '{model_name}'")
            print(f"   📝 Code à utiliser:")
            print(f"      client = genai.Client(api_key=...)")
            print(f"      response = client.models.generate_content(")
            print(f"          model='{model_name}',")
            print(f"          contents=prompt")
            print(f"      )")
            return  # Arrêter au premier qui fonctionne
        except Exception as e:
            print(f"   ❌ Erreur: {str(e)[:100]}")
    
    print("\n" + "=" * 60)
    print("🧪 Test avec l'ANCIENNE syntaxe (GenerativeModel)")
    print("=" * 60)
    
    try:
        genai.configure(api_key=Config.GEMINI_API_KEY)
        print("✅ Configuration OK")
    except Exception as e:
        print(f"❌ Erreur configuration: {e}")
        return
    
    # Liste des modèles à tester avec l'ancienne syntaxe
    old_models = [
        'gemini-pro',
        'gemini-1.5-pro',
        'gemini-1.5-flash',
        'gemini-1.5-flash-latest',
        'gemini-1.0-pro',
    ]
    
    for model_name in old_models:
        print(f"\n🔍 Test de '{model_name}' avec GenerativeModel()...")
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Dis bonjour en français")
            print(f"   ✅ Fonctionne ! Réponse: {response.text[:50]}...")
            print(f"   👉 Utilisez ce modèle: '{model_name}'")
            return  # Arrêter au premier qui fonctionne
        except Exception as e:
            print(f"   ❌ Erreur: {str(e)[:100]}")
    
    print("\n" + "=" * 60)
    print("\n💡 Recommandation:")
    print("   Mettez à jour backend/services/gemini_service.py")
    print("   avec le nom du modèle qui fonctionne.")
    print("=" * 60)

if __name__ == '__main__':
    print("🚀 Test de l'API Gemini\n")
    test_gemini()
    print("\n✅ Test terminé !")
