"""
Test GCP TTS and STT API Keys
"""
import os
import asyncio
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_gcp_tts():
    """Test GCP Text-to-Speech API"""
    api_key = os.getenv("GCP_TTS_API_KEY")
    base_url = "https://texttospeech.googleapis.com/v1"
    
    print("\n" + "="*60)
    print("Testing GCP Text-to-Speech API")
    print("="*60)
    print(f"API Key: {api_key[:20] if api_key else 'NOT SET'}...")
    print(f"Base URL: {base_url}")
    
    if not api_key:
        print("[ERROR] GCP_TTS_API_KEY not set in .env file")
        return False
    
    # Remove quotes if present
    api_key = api_key.strip('"').strip("'")
    
    url = f"{base_url}/text:synthesize"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key
    }
    
    payload = {
        "input": {"text": "Hello, testing GCP TTS."},
        "voice": {
            "languageCode": "en-US",
            "name": "en-US-Neural2-F"
        },
        "audioConfig": {
            "audioEncoding": "MP3"
        }
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                json=payload,
                timeout=30.0
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("[OK] GCP TTS API is working!")
                return True
            else:
                print(f"[FAIL] GCP TTS API failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"[ERROR] Exception testing GCP TTS: {e}")
        return False


async def test_gcp_stt():
    """Test GCP Speech-to-Text API"""
    api_key = os.getenv("GCP_STT_API_KEY")
    base_url = "https://speech.googleapis.com/v1"
    
    print("\n" + "="*60)
    print("Testing GCP Speech-to-Text API")
    print("="*60)
    print(f"API Key: {api_key[:20] if api_key else 'NOT SET'}...")
    print(f"Base URL: {base_url}")
    
    if not api_key:
        print("[ERROR] GCP_STT_API_KEY not set in .env file")
        return False
    
    # Remove quotes if present
    api_key = api_key.strip('"').strip("'")
    
    # Try a simple API call to check authentication
    url = f"{base_url}/operations"
    headers = {
        "X-Goog-Api-Key": api_key
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers=headers,
                timeout=30.0
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code in [200, 400]:  # 400 might mean API is reachable but request format issue
                print("[OK] GCP STT API is reachable!")
                return True
            else:
                print(f"[FAIL] GCP STT API failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"[ERROR] Exception testing GCP STT: {e}")
        return False


async def test_gemini():
    """Test Gemini API as a control"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    print("\n" + "="*60)
    print("Testing Gemini API (Control)")
    print("="*60)
    print(f"API Key: {api_key[:20] if api_key else 'NOT SET'}...")
    
    if not api_key:
        print("[ERROR] GEMINI_API_KEY not set")
        return False
    
    # Remove quotes if present
    api_key = api_key.strip('"').strip("'")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("[OK] Gemini API is working!")
                return True
            else:
                print(f"[FAIL] Gemini API failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"[ERROR] Exception testing Gemini: {e}")
        return False


async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("GCP API Testing Script")
    print("="*60)
    
    # Test Gemini first (should work)
    gemini_ok = await test_gemini()
    
    # Test GCP APIs
    tts_ok = await test_gcp_tts()
    stt_ok = await test_gcp_stt()
    
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    print(f"Gemini API: {'[OK]' if gemini_ok else '[FAILED]'}")
    print(f"GCP TTS API: {'[OK]' if tts_ok else '[FAILED]'}")
    print(f"GCP STT API: {'[OK]' if stt_ok else '[FAILED]'}")
    print("="*60)
    
    if not tts_ok or not stt_ok:
        print("\n💡 TROUBLESHOOTING:")
        print("1. Check if GCP_TTS_API_KEY and GCP_STT_API_KEY are correct")
        print("2. Ensure the APIs are enabled in Google Cloud Console:")
        print("   - Cloud Text-to-Speech API")
        print("   - Cloud Speech-to-Text API")
        print("3. Verify the API keys have proper permissions")
        print("4. Check if there are any quotes in the .env file (remove them)")


if __name__ == "__main__":
    asyncio.run(main())
