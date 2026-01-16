"""Test GCP STT provider"""
import asyncio
import os
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from app.services.voice_providers.gcp_stt import GCPSTTProvider


async def test_stt():
    """Test GCP STT provider initialization and health check."""
    try:
        print("Initializing GCP STT Provider...")
        provider = GCPSTTProvider()
        print("✅ Provider initialized successfully")
        
        print("\nRunning health check...")
        is_healthy = await provider.health_check()
        print(f"Health check result: {'✅ Healthy' if is_healthy else '❌ Unhealthy'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_stt())
