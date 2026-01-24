"""
Google Gemini 3 Pro Image - IMPROVED Avatar Generation Implementation
Fixes identity preservation by passing source images to generation model

CRITICAL IMPROVEMENTS:
1. ✅ Passes source image directly to generation model (not just text description)
2. ✅ Improved vision prompts for better feature extraction
3. ✅ Avatar generation prompt with identity preservation directives
4. ✅ Better error handling and logging
5. ✅ Support for both photo and hand-drawn sources

The key fix: Original image is now kept and passed alongside text to generation,
allowing model to preserve identity while applying style.
"""

import os
import base64
import httpx
import asyncio
from typing import Optional
from dataclasses import dataclass


@dataclass
class ImageGenerationRequest:
    """Image generation request with style and parameters"""
    prompt: str
    style: str = "cartoon"
    width: int = 512
    height: int = 512
    source_image_base64: Optional[str] = None      # ✅ NEW: Source image reference
    source_mime_type: str = "image/png"            # ✅ NEW: Image MIME type


class GeminiImagenProviderImproved:
    """
    IMPROVED Gemini 3 Pro Image Avatar Generation
    
    Key Improvement: Passes source image directly to generation model
    This preserves identity much better than text-only descriptions
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_IMAGE_MODEL", "gemini-3-pro-image-preview")
        self.vision_model = os.getenv("GEMINI_MODEL", "gemini-3-pro-preview")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")

    async def generate_image(self, request: ImageGenerationRequest) -> bytes:
        """
        Generate image using Gemini 3 Pro with optional reference image
        
        ✅ CRITICAL FIX: If source_image_base64 is provided, we pass it to the 
        generation model so it can use both the image AND the text description
        """
        url = f"{self.base_url}/models/{self.model}:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }

        # ✅ Build parts array with image (if provided) and text
        parts = []
        
        # ✅ Add source image as reference if provided (use hasattr for compatibility)
        source_image = getattr(request, 'source_image_base64', None)
        if source_image:
            mime_type = getattr(request, 'source_mime_type', 'image/png')
            parts.append({
                "inlineData": {
                    "mimeType": mime_type,
                    "data": source_image
                }
            })
        
        # Add text prompt
        parts.append({
            "text": request.prompt
        })

        # Build payload
        payload = {
            "contents": [{
                "role": "user",
                "parts": parts  # ✅ BOTH image and text together
            }],
            "generationConfig": {
                "responseModalities": ["TEXT", "IMAGE"],
                "temperature": 0.4
            }
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

                # Extract image from response
                if "candidates" in data and len(data["candidates"]) > 0:
                    candidate = data["candidates"][0]
                    parts_response = candidate.get("content", {}).get("parts", [])
                    
                    for part in parts_response:
                        if "inlineData" in part:
                            inline_data = part["inlineData"]
                            if "data" in inline_data:
                                return base64.b64decode(inline_data["data"])
                
                raise ValueError("No image data found in Gemini API response")

            except httpx.HTTPStatusError as e:
                error_detail = e.response.text
                raise ValueError(f"Gemini API HTTP Error {e.response.status_code}: {error_detail}")
            except Exception as e:
                raise ValueError(f"Image generation failed: {str(e)}")

    async def analyze_source_image(self, source_image_bytes: bytes) -> dict:
        """
        Analyze source image to extract key features for avatar generation
        
        ✅ IMPROVED: Better extraction of distinctive features
        
        Returns dict with:
        - description: Text description of key features
        - source_type: 'photo', 'sketch', 'drawing', or 'abstract'
        - source_base64: Base64 encoded image for passing to generation
        - mime_type: Detected MIME type
        """
        vision_url = f"{self.base_url}/models/{self.vision_model}:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }

        # Detect MIME type
        mime_type = self._detect_mime_type(source_image_bytes)
        source_base64 = base64.b64encode(source_image_bytes).decode('utf-8')

        # ✅ IMPROVED vision analysis prompt
        vision_prompt = """Analyze this image as reference for avatar creation. Provide structured analysis:

**Subject Type**: Is this a photo of person/animal, hand-drawn sketch, doodle, abstract, or something else?

**Facial/Physical Features** (if applicable):
- Face shape and proportions
- Distinctive features (scars, glasses, birthmarks, unique facial characteristics)
- Hair: color, style, texture (specific style like bob, ponytail, buzzcut?)
- Skin tone and complexion
- Expression: happy, neutral, serious, playful?
- Eye color and shape
- Any asymmetries or unique proportions

**Color Palette**: 
- Primary colors used
- Color scheme (warm, cool, neutral)
- Notable color combinations

**Overall Style Assessment**:
- Art style of source (realistic, stylized, minimalist, detailed, sketch-like)
- Unique artistic elements
- Quality and clarity

**What Makes This Unique**: 
In 1-2 sentences, what would make this recognizable/distinctive in an avatar?

Keep analysis under 150 words, focusing on elements that MUST be preserved."""

        vision_payload = {
            "contents": [{
                "parts": [
                    {
                        "inlineData": {
                            "mimeType": mime_type,
                            "data": source_base64
                        }
                    },
                    {
                        "text": vision_prompt
                    }
                ]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 300
            }
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    vision_url,
                    headers=headers,
                    json=vision_payload,
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                
                description = data["candidates"][0]["content"]["parts"][0]["text"]
                
                # Parse source type from description
                description_lower = description.lower()
                source_type = "unknown"
                if "photo" in description_lower or "photograph" in description_lower:
                    source_type = "photo"
                elif "sketch" in description_lower or "drawn" in description_lower:
                    source_type = "sketch"
                elif "abstract" in description_lower:
                    source_type = "abstract"
                else:
                    source_type = "image"
                
                return {
                    "description": description,
                    "source_type": source_type,
                    "mime_type": mime_type,
                    "source_base64": source_base64
                }
                
            except Exception as e:
                print(f"[WARNING] Vision analysis failed: {e}")
                return {
                    "description": "Unable to analyze - using generic avatar generation",
                    "source_type": "unknown",
                    "mime_type": mime_type,
                    "source_base64": source_base64
                }

    async def generate_avatar(
        self,
        source_image: bytes,
        style: str = "cartoon",
        custom_prompt: str = ""
    ) -> bytes:
        """
        ✅ IMPROVED: Generate avatar from source image
        
        Key Improvement:
        1. Analyzes source image for key features
        2. Passes BOTH source image AND description to generation model
        3. This preserves identity much better than text-only
        
        Args:
            source_image: Source image bytes (photo, sketch, drawing, etc.)
            style: 'cartoon' or 'realistic'
            custom_prompt: Optional user instruction (e.g., "make me a superhero")
        
        Returns:
            Avatar image bytes
        """
        print(f"[INFO] Starting avatar generation - style: {style}")
        
        # Step 1: Analyze source image
        analysis = await self.analyze_source_image(source_image)
        description = analysis["description"]
        source_type = analysis["source_type"]
        source_base64 = analysis["source_base64"]
        mime_type = analysis["mime_type"]
        
        print(f"[INFO] Source analysis complete - type: {source_type}")
        print(f"[DEBUG] Analysis:\n{description[:200]}...")

        # Step 2: Build avatar generation prompt
        if style == "cartoon":
            style_directive = """Generate a cartoon avatar that:
- Has vibrant, appealing colors
- Maintains expressive, friendly features
- Uses clean lines and simplified shapes
- Is suitable for animation/gaming
- Preserves the key characteristics and personality of the source"""
        elif style == "realistic":
            style_directive = """Generate a realistic portrait avatar that:
- Maintains photorealistic quality
- Preserves facial structure and distinctive features
- Uses natural lighting and professional photography style
- Shows detailed, accurate features
- Maintains the essence and character of the source"""
        else:
            style_directive = "Generate a stylized avatar preserving source characteristics"

        # ✅ IMPROVED avatar generation prompt with identity preservation
        base_prompt = f"""You are an expert avatar artist. Create a stunning avatar based on the reference image provided.

{style_directive}

**Reference Image Analysis**:
{description}

**Requirements**:
1. The avatar MUST be recognizable as the same person/subject in the reference image
2. Preserve distinctive features: facial structure, unique characteristics, expression
3. Apply the {style} style while maintaining identity
4. Suitable for profile picture: centered composition, clean background
5. Professional quality output"""

        if custom_prompt.strip():
            full_prompt = f"""{base_prompt}

**User's Additional Instructions**:
{custom_prompt}

Incorporate these instructions while maintaining the core identity and characteristics from the reference image."""
        else:
            full_prompt = f"""{base_prompt}

Make it polished, professional, and immediately usable as a profile picture."""

        print(f"[DEBUG] Avatar prompt:\n{full_prompt[:300]}...")

        # Step 3: Generate avatar with ✅ source image reference
        request = ImageGenerationRequest(
            prompt=full_prompt,
            style=style,
            width=512,
            height=512,
            source_image_base64=source_base64,  # ✅ PASS IMAGE
            source_mime_type=mime_type
        )

        try:
            avatar_bytes = await self.generate_image(request)
            print(f"[INFO] Avatar generated successfully - size: {len(avatar_bytes)} bytes")
            return avatar_bytes
        except Exception as e:
            print(f"[ERROR] Avatar generation failed: {e}")
            print(f"[INFO] Attempting fallback generation...")
            
            # Fallback: Try without source image reference
            fallback_prompt = f"""Create a {style} avatar profile picture.
            
Source characteristics: {description}
User request: {custom_prompt if custom_prompt else 'Professional avatar'}

Make it friendly, appealing, and suitable for profile use."""
            
            fallback_request = ImageGenerationRequest(
                prompt=fallback_prompt,
                style=style,
                width=512,
                height=512
            )
            
            try:
                return await self.generate_image(fallback_request)
            except Exception as fallback_error:
                raise ValueError(f"Avatar generation failed (primary and fallback): {str(e)} | Fallback: {str(fallback_error)}")

    async def generate_character(
        self,
        source_image: bytes,
        style: str = "cartoon",
        custom_prompt: str = "",
        character_name: str = "",
        character_description: str = ""
    ) -> bytes:
        """
        Generate a full-body story character from source image (upload or drawing).
        
        Unlike avatars (face-focused, clean background), characters are:
        - Full body with dynamic poses
        - Include contextual backgrounds
        - Designed for story/educational illustration
        
        Args:
            source_image: Source image bytes (photo, sketch, drawing)
            style: 'cartoon' or 'realistic'
            custom_prompt: Optional user instructions
            character_name: Name of the character (for context)
            character_description: Description/role of character
        
        Returns:
            Character image bytes (768x1024 portrait orientation)
        """
        print(f"[INFO] Starting character generation - style: {style}, name: {character_name}")
        
        # Step 1: Analyze source image
        analysis = await self.analyze_source_image(source_image)
        description = analysis["description"]
        source_type = analysis["source_type"]
        source_base64 = analysis["source_base64"]
        mime_type = analysis["mime_type"]
        
        print(f"[INFO] Source analysis complete - type: {source_type}")
        
        # Step 2: Build character generation prompt (different from avatar!)
        if style == "cartoon":
            style_directive = """Generate a FULL BODY cartoon character that:
- Shows the complete character from head to feet
- Has a dynamic, expressive pose suitable for storytelling
- Uses vibrant, child-friendly colors
- Includes an appropriate background scene (classroom, nature, adventure setting, etc.)
- Has the style of modern animated movies (Pixar/Disney quality)
- Is suitable for educational children's content
- Preserves key characteristics from the source image"""
        elif style == "realistic":
            style_directive = """Generate a FULL BODY realistic character illustration that:
- Shows the complete character from head to feet
- Has a natural, engaging pose
- Uses realistic proportions and detailed features
- Includes a contextual background environment
- Has professional illustration quality
- Is suitable for educational content
- Preserves key characteristics from the source image"""
        else:
            style_directive = "Generate a full body character illustration with background"

        # Build character context
        character_context = ""
        if character_name:
            character_context += f"\n**Character Name**: {character_name}"
        if character_description:
            character_context += f"\n**Character Role**: {character_description}"

        # Build the full prompt for character generation
        base_prompt = f"""You are an expert character designer for educational children's content. 
Create a full-body story character based on the reference image provided.

{style_directive}
{character_context}

**Reference Image Analysis**:
{description}

**IMPORTANT Requirements**:
1. FULL BODY: Show the character from head to feet, not just face
2. POSE: Give the character an engaging, dynamic pose (waving, pointing, teaching, exploring, etc.)
3. BACKGROUND: Include an appropriate scene background (not plain/clean like avatars)
4. IDENTITY: Preserve distinctive features and personality from the source
5. STYLE: Apply {style} style consistently throughout
6. PURPOSE: This character will appear in educational learning stories"""

        if custom_prompt.strip():
            full_prompt = f"""{base_prompt}

**User's Special Instructions**:
{custom_prompt}

Incorporate these instructions while maintaining the character's recognizability and educational appropriateness."""
        else:
            full_prompt = f"""{base_prompt}

Make the character friendly, approachable, and perfect for appearing in children's learning adventures."""

        print(f"[DEBUG] Character prompt:\n{full_prompt[:400]}...")

        # Step 3: Generate character with source image reference
        # Use portrait orientation for full-body characters
        request = ImageGenerationRequest(
            prompt=full_prompt,
            style=style,
            width=768,   # Portrait orientation for full body
            height=1024,
            source_image_base64=source_base64,
            source_mime_type=mime_type
        )

        try:
            character_bytes = await self.generate_image(request)
            print(f"[INFO] Character generated successfully - size: {len(character_bytes)} bytes")
            return character_bytes
        except Exception as e:
            print(f"[ERROR] Character generation failed: {e}")
            print(f"[INFO] Attempting fallback generation...")
            
            # Fallback without source image
            fallback_prompt = f"""Create a {style} full-body character illustration.

Character: {character_name or 'Friendly helper character'}
Description: {character_description or 'A friendly character for learning stories'}
User request: {custom_prompt if custom_prompt else 'Make it appealing and educational'}

Requirements:
- Full body shown (head to feet)
- Dynamic, engaging pose
- Include background scene
- Child-friendly and educational style"""
            
            fallback_request = ImageGenerationRequest(
                prompt=fallback_prompt,
                style=style,
                width=768,
                height=1024
            )
            
            try:
                return await self.generate_image(fallback_request)
            except Exception as fallback_error:
                raise ValueError(f"Character generation failed: {str(e)} | Fallback: {str(fallback_error)}")

    async def stylize_character(
        self,
        source_image: bytes,
        style: str = "cartoon"
    ) -> bytes:
        """
        Convert uploaded image or drawing to character using Gemini 3 Pro.
        
        Args:
            source_image: Source image bytes
            style: Character style (cartoon or realistic)
        
        Returns:
            Stylized character image bytes
        """
        # Analyze image first
        analysis = await self.analyze_source_image(source_image)
        description = analysis["description"]
        source_base64 = analysis["source_base64"]
        mime_type = analysis["mime_type"]
        
        if style == "cartoon":
            style_description = "cartoon character illustration, animated style, colorful, expressive, digital art"
        elif style == "realistic":
            style_description = "realistic character illustration, detailed, high quality, professional artwork"
        else:
            style_description = "stylized character illustration, high quality"

        prompt = f"""Create a {style_description}, full body character, clean background, 
suitable for story illustration. Preserve key characteristics from the reference image."""

        request = ImageGenerationRequest(
            prompt=prompt,
            style=style,
            width=1024,
            height=1024,
            source_image_base64=source_base64,  # ✅ PASS IMAGE
            source_mime_type=mime_type
        )

        return await self.generate_image(request)

    def _detect_mime_type(self, image_bytes: bytes) -> str:
        """Detect image MIME type from magic bytes"""
        if image_bytes[:3] == b'\xff\xd8\xff':
            return "image/jpeg"
        elif image_bytes[:4] == b'\x89PNG':
            return "image/png"
        elif image_bytes[:4] == b'GIF8':
            return "image/gif"
        elif image_bytes[:4] == b'RIFF' and image_bytes[8:12] == b'WEBP':
            return "image/webp"
        else:
            return "image/png"

    async def health_check(self) -> bool:
        """Check if Gemini API is accessible"""
        try:
            url = f"{self.base_url}/models"
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{url}?key={self.api_key}",
                    timeout=10.0
                )
            return response.status_code == 200
        except Exception:
            return False


# For backward compatibility
GeminiImagenProvider = GeminiImagenProviderImproved
