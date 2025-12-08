
import asyncio
import sys
import os
import httpx
import time

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from analysis.services.huggingface import HuggingFaceService
from config import get_settings

async def test_huggingface_connection():
    print("=== Testing Hugging Face API Integration ===")
    settings = get_settings()
    print(f"Model: {settings.huggingface_model}")
    print(f"Timeout: {settings.huggingface_timeout}s")
    
    service = HuggingFaceService()
    
    text = "Artificial intelligence is transforming the world."
    labels = ["Technology", "Politics", "Sports", "Health"]
    
    print(f"\nSending classification request...")
    print(f"Text: '{text}'")
    print(f"Candidate Labels: {labels}")
    
    start_time = time.time()
    try:
        result = await service.classify(text, labels)
        duration = time.time() - start_time
        print(f"\n✅ Classification Successful! (took {duration:.2f}s)")
        print("-" * 30)
        print(f"Category: {result['category']}")
        print(f"Score: {result['score']:.4f}")
        print("-" * 30)
    except Exception as e:
        duration = time.time() - start_time
        print(f"\n❌ Error during classification (after {duration:.2f}s): {e}")

if __name__ == "__main__":
    asyncio.run(test_huggingface_connection())
