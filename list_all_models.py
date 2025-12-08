
import google.generativeai as genai
import sys
import os

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from backend.config import get_settings

def list_all_models():
    settings = get_settings()
    genai.configure(api_key=settings.gemini_api_key)
    
    print("=== Available Gemini Models ===")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Name: {m.name}")
                # print(f"Display Name: {m.displayName}")
                # print(f"Description: {m.description[:50]}...")
                print("-" * 20)
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_all_models()
