#!/usr/bin/env python3
"""Test Gemini Models with provided API key"""

import google.generativeai as genai

API_KEY = "AIzaSyAPdNaogkzkuANFAgxyqRzBDUSaOUkUOw4"
TEXT_MODEL = "gemini-3-pro-preview"
IMAGE_MODEL = "gemini-3-pro-image-preview"

def main():
    print("=" * 50)
    print("Gemini Model Test")
    print("=" * 50)
    
    genai.configure(api_key=API_KEY)
    
    # Test 1: Text Model
    print(f"\n[1] Testing: {TEXT_MODEL}")
    print("-" * 40)
    try:
        model = genai.GenerativeModel(TEXT_MODEL)
        response = model.generate_content("Say hello in one word")
        print(f"✅ SUCCESS!")
        print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    # Test 2: Image Model
    print(f"\n[2] Testing: {IMAGE_MODEL}")
    print("-" * 40)
    try:
        img_model = genai.GenerativeModel(IMAGE_MODEL)
        response2 = img_model.generate_content("Describe a simple red circle")
        print(f"✅ SUCCESS!")
        if hasattr(response2, 'text'):
            print(f"Response: {response2.text[:200]}")
        else:
            print(f"Response: {str(response2)[:200]}")
    except Exception as e:
        print(f"❌ FAILED: {e}")
    
    print("\n" + "=" * 50)
    print("Test Complete")
    print("=" * 50)

if __name__ == "__main__":
    main()
