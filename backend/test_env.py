"""Test script to verify environment configuration."""
import sys
from config import get_settings

def test_environment():
    """Test if environment variables are properly configured."""
    print("=== Environment Configuration Status ===\n")
    
    try:
        s = get_settings()
        print("✓ Configuration loaded successfully\n")
        
        # Check JWT Secret
        if s.jwt_secret == "your-secret-key-change-this-in-production":
            print("⚠️  JWT Secret: USING DEFAULT (change this for production!)")
        else:
            print(f"✓ JWT Secret: SET ({len(s.jwt_secret)} chars)")
        
        # Check API Keys
        if s.huggingface_api_token:
            print(f"✓ HuggingFace Token: SET ({s.huggingface_api_token[:8]}...)")
        else:
            print("❌ HuggingFace Token: NOT SET")
        
        if s.gemini_api_key:
            print(f"✓ Gemini API Key: SET ({s.gemini_api_key[:8]}...)")
        else:
            print("❌ Gemini API Key: NOT SET")
        
        # Check Database
        print(f"✓ Database URL: {s.database_url[:40]}...")
        
        # Check CORS
        print(f"✓ CORS Origins: {s.cors_origins}")
        
        # Check other settings
        print(f"✓ HuggingFace Model: {s.huggingface_model}")
        print(f"✓ Log Level: {s.log_level}")
        print(f"✓ JWT Algorithm: {s.jwt_algorithm}")
        print(f"✓ JWT Expiration: {s.jwt_expiration_minutes} minutes")
        
        # Summary
        print("\n=== Summary ===")
        missing = []
        if not s.huggingface_api_token:
            missing.append("HuggingFace API Token")
        if not s.gemini_api_key:
            missing.append("Gemini API Key")
        if s.jwt_secret == "your-secret-key-change-this-in-production":
            missing.append("JWT Secret (using default)")
        
        if missing:
            print(f"⚠️  Missing or default values: {', '.join(missing)}")
            print("\nTo fix:")
            print("1. Get HuggingFace token: https://huggingface.co/settings/tokens")
            print("2. Get Gemini API key: https://aistudio.google.com/app/apikey")
            print("3. Update your .env file with these values")
            return False
        else:
            print("✅ All required environment variables are set!")
            print("✅ Backend is ready to start!")
            return True
            
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return False

if __name__ == "__main__":
    success = test_environment()
    sys.exit(0 if success else 1)
