"""
FIBO Image Provider Implementation - IMPROVED
Avatar generation with identity preservation

IMPROVEMENTS:
1. ✅ Enhanced stylization pipeline
2. ✅ Better prompt engineering for avatar generation
3. ✅ Improved error handling and logging
4. ✅ Support for various image formats and sources
5. ✅ Identity preservation through detailed prompts
"""

import os
import base64
import httpx
from typing import Optional
from dataclasses import dataclass


@dataclass
class ImageGenerationRequest:
    """Image generation request with style and parameters"""
    prompt: str
    style: str = "cartoon"
    width: int = 512
    height: int = 512
    source_image_base64: Optional[str] = None
    source_mime_type: str = "image/png"


class FiboProviderImproved:
    """
    ✅ IMPROVED FIBO API implementation for image generation.
    
    Enhancements:
    - Better avatar generation with identity preservation
    - Improved stylization prompts
    - Enhanced error handling
    - Logging and debugging support
    """

    def __init__(self):
        self.api_key = os.getenv("FIBO_API_KEY")
        self.base_url = os.getenv("FIBO_API_ENDPOINT", "https://api.fibo.ai/v1")
        if not self.api_key:
            raise ValueError("FIBO_API_KEY environment variable not set")

    async def generate_image(self, request: ImageGenerationRequest) -> bytes:
        """
        Generate an image using FIBO API.
        
        Args:
            request: Image generation request with prompt and parameters
        
        Returns:
            Image bytes (PNG format)
        """
        url = f"{self.base_url}/images/generate"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Enhance prompt based on style
        style_prefix = ""
        if request.style == "cartoon":
            style_prefix = "Cartoon style, colorful, animated, child-friendly, vibrant: "
        elif request.style == "realistic":
            style_prefix = "Realistic style, photographic, detailed, high quality: "
        
        full_prompt = style_prefix + request.prompt

        payload = {
            "prompt": full_prompt,
            "width": request.width,
            "height": request.height,
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=120.0
                )
                response.raise_for_status()
                data = response.json()

                # FIBO typically returns image URL or base64
                if "url" in data:
                    image_response = await client.get(data["url"], timeout=60.0)
                    image_response.raise_for_status()
                    return image_response.content
                
                elif "image" in data:
                    return base64.b64decode(data["image"])
                
                elif response.headers.get("content-type", "").startswith("image/"):
                    return response.content
                
                raise ValueError("Unexpected response format from FIBO API")
            
            except httpx.HTTPStatusError as e:
                raise ValueError(f"FIBO API HTTP Error {e.response.status_code}: {e.response.text}")
            except Exception as e:
                raise ValueError(f"Image generation failed: {str(e)}")

    async def generate_avatar(
        self,
        source_image: bytes,
        style: str = "cartoon",
        custom_prompt: str = ""
    ) -> bytes:
        """
        ✅ IMPROVED: Generate avatar from source image using FIBO.
        
        Key improvements:
        - Better prompt engineering for identity preservation
        - Enhanced stylization with detailed instructions
        - Improved error handling
        
        Args:
            source_image: Source image bytes
            style: Avatar style (cartoon or realistic)
            custom_prompt: Optional custom instructions from user
        
        Returns:
            Avatar image bytes
        """
        print(f"[INFO] Starting avatar generation with FIBO - style: {style}")
        
        url = f"{self.base_url}/images/stylize"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        # Create multipart form data
        files = {
            "image": ("source.png", source_image, "image/png")
        }

        # ✅ IMPROVED: Build detailed style prompt for better identity preservation
        if style == "cartoon":
            style_prompt = """Transform into a cartoon avatar that:
- Preserves the key characteristics and personality of the source person
- Uses vibrant, appealing colors
- Has an expressive, friendly animated character style
- Maintains facial structure and distinctive features
- Is suitable for animation or gaming"""
        elif style == "realistic":
            style_prompt = """Transform into a realistic portrait avatar that:
- Preserves facial structure and distinctive features from source
- Maintains photorealistic quality with detailed features
- Uses professional headshot style
- Shows natural lighting and proportions
- Is suitable for professional profile pictures"""
        else:
            style_prompt = "Transform into an avatar style while preserving source characteristics"

        # Combine with custom prompt if provided
        if custom_prompt.strip():
            style_prompt = f"""{style_prompt}

Additional user instructions: {custom_prompt}

Balance these instructions while maintaining the recognizability of the original person."""

        data = {
            "prompt": style_prompt,
            "style": style,
        }

        async with httpx.AsyncClient() as client:
            try:
                print(f"[DEBUG] Avatar prompt: {style_prompt[:150]}...")
                
                response = await client.post(
                    url,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=120.0
                )
                response.raise_for_status()
                response_data = response.json()

                # Handle response similar to generate_image
                if "url" in response_data:
                    image_response = await client.get(response_data["url"], timeout=60.0)
                    image_response.raise_for_status()
                    avatar_bytes = image_response.content
                
                elif "image" in response_data:
                    avatar_bytes = base64.b64decode(response_data["image"])
                
                elif response.headers.get("content-type", "").startswith("image/"):
                    avatar_bytes = response.content
                
                else:
                    raise ValueError("Unexpected response format from FIBO API")
                
                print(f"[INFO] Avatar generated successfully - size: {len(avatar_bytes)} bytes")
                return avatar_bytes
            
            except httpx.HTTPStatusError as e:
                print(f"[ERROR] FIBO API HTTP Error {e.response.status_code}")
                raise ValueError(f"Avatar generation failed: {e.response.text}")
            except Exception as e:
                print(f"[ERROR] Avatar generation failed: {e}")
                raise ValueError(f"Avatar generation failed: {str(e)}")

    async def generate_character(
        self,
        source_image: bytes,
        style: str = "cartoon",
        custom_prompt: str = "",
        character_name: str = "",
        character_description: str = ""
    ) -> bytes:
        """
        Generate a full-body story character from source image.
        
        Unlike avatars, characters are full-body with backgrounds.
        
        Args:
            source_image: Source image bytes
            style: 'cartoon' or 'realistic'
            custom_prompt: Optional user instructions
            character_name: Name of the character
            character_description: Description/role of character
        
        Returns:
            Character image bytes
        """
        print(f"[INFO] Starting character generation with FIBO - style: {style}")
        
        url = f"{self.base_url}/images/stylize"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        files = {
            "image": ("source.png", source_image, "image/png")
        }

        # Build full-body character prompt
        if style == "cartoon":
            style_prompt = """Transform into a FULL BODY cartoon character that:
- Shows complete character from head to feet
- Has a dynamic, expressive pose
- Uses vibrant, child-friendly colors
- Includes an appropriate background scene
- Preserves key characteristics from the source
- Suitable for educational children's content"""
        elif style == "realistic":
            style_prompt = """Transform into a FULL BODY realistic character illustration that:
- Shows complete character from head to feet
- Has an engaging, natural pose
- Uses realistic proportions and details
- Includes a contextual background
- Preserves key characteristics from the source
- Suitable for educational content"""
        else:
            style_prompt = "Transform into a full body character with background scene"

        # Add character context
        if character_name:
            style_prompt += f"\n\nCharacter Name: {character_name}"
        if character_description:
            style_prompt += f"\nCharacter Role: {character_description}"

        # Combine with custom prompt
        if custom_prompt.strip():
            style_prompt = f"""{style_prompt}

User's special instructions: {custom_prompt}"""

        data = {
            "prompt": style_prompt,
            "style": style,
        }

        async with httpx.AsyncClient() as client:
            try:
                print(f"[DEBUG] Character prompt: {style_prompt[:150]}...")
                
                response = await client.post(
                    url,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=120.0
                )
                response.raise_for_status()
                response_data = response.json()

                if "url" in response_data:
                    image_response = await client.get(response_data["url"], timeout=60.0)
                    image_response.raise_for_status()
                    character_bytes = image_response.content
                
                elif "image" in response_data:
                    character_bytes = base64.b64decode(response_data["image"])
                
                elif response.headers.get("content-type", "").startswith("image/"):
                    character_bytes = response.content
                
                else:
                    raise ValueError("Unexpected response format from FIBO API")
                
                print(f"[INFO] Character generated successfully - size: {len(character_bytes)} bytes")
                return character_bytes
            
            except Exception as e:
                print(f"[ERROR] Character generation failed: {e}")
                raise ValueError(f"Character generation failed: {str(e)}")

    async def stylize_character(
        self,
        source_image: bytes,
        style: str = "cartoon"
    ) -> bytes:
        """
        ✅ IMPROVED: Convert uploaded image or drawing to character using FIBO.
        
        Args:
            source_image: Source image bytes
            style: Character style (cartoon or realistic)
        
        Returns:
            Stylized character image bytes
        """
        print(f"[INFO] Starting character stylization with FIBO - style: {style}")
        
        url = f"{self.base_url}/images/stylize"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        files = {
            "image": ("source.png", source_image, "image/png")
        }

        # ✅ IMPROVED: Better character style prompts
        if style == "cartoon":
            style_prompt = """Transform into a cartoon character illustration with:
- Animated style, colorful and expressive
- Vibrant, appealing character design
- Clean lines and stylized features
- Suitable for storytelling or entertainment
- Maintain personality and key characteristics"""
        elif style == "realistic":
            style_prompt = """Transform into a realistic character illustration with:
- Detailed, high quality artwork
- Professional character design
- Natural lighting and proportions
- Suitable for concept art
- Maintain realistic features and characteristics"""
        else:
            style_prompt = "Transform into a stylized character illustration"

        data = {
            "prompt": style_prompt,
            "style": style,
        }

        async with httpx.AsyncClient() as client:
            try:
                print(f"[DEBUG] Character prompt: {style_prompt[:150]}...")
                
                response = await client.post(
                    url,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=120.0
                )
                response.raise_for_status()
                response_data = response.json()

                if "url" in response_data:
                    image_response = await client.get(response_data["url"], timeout=60.0)
                    image_response.raise_for_status()
                    character_bytes = image_response.content
                
                elif "image" in response_data:
                    character_bytes = base64.b64decode(response_data["image"])
                
                elif response.headers.get("content-type", "").startswith("image/"):
                    character_bytes = response.content
                
                else:
                    raise ValueError("Unexpected response format from FIBO API")
                
                print(f"[INFO] Character generated successfully - size: {len(character_bytes)} bytes")
                return character_bytes
            
            except Exception as e:
                print(f"[ERROR] Character stylization failed: {e}")
                raise ValueError(f"Character stylization failed: {str(e)}")

    async def health_check(self) -> bool:
        """Check if FIBO API is accessible."""
        try:
            url = f"{self.base_url}/health"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, timeout=10.0)
            return response.status_code == 200
        except Exception:
            return False


# For backward compatibility
FiboProvider = FiboProviderImproved
