
import asyncio
import sys
import os
import google.generativeai as genai

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__)))
from config import get_settings

async def test_gemini_2_5():
    settings = get_settings()
    genai.configure(api_key=settings.gemini_api_key)
    
    print("=== Testing Gemini 2.5 Flash ===")
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    text = "Machine learning makes software smarter."
    prompt = f"Summarize this: {text}"
    
    print("Sending request...")
    try:
        response = model.generate_content(prompt)
        print("\n✅ Success!")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini_2_5())
