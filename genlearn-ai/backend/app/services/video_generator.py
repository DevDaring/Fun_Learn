"""
Video Generator Service
Combines images and audio into 8-second videos using FFmpeg
"""

import asyncio
import subprocess
import os
from typing import Any, Optional
from pathlib import Path
from datetime import datetime

from app.services.provider_factory import ProviderFactory
from app.database.csv_handler import (
    get_sessions_handler,
    get_learning_history_handler
)
from app.database.file_handler import save_generated_video, FileHandler
from app.config import settings


class VideoGenerator:
    """
    Service for generating videos from images and audio.

    Responsibilities:
    - Generate audio narration using TTS provider
    - Combine images with audio using FFmpeg
    - Create 8-second video segments
    - Save videos and track in history
    """

    def __init__(self):
        """Initialize the video generator service."""
        self.tts_provider = ProviderFactory.get_tts_provider()
        self.sessions_handler = get_sessions_handler()
        self.history_handler = get_learning_history_handler()

    async def generate_video_for_cycle(
        self,
        session_id: str,
        cycle_number: int,
        image_urls: list[str],
        narratives: list[str],
        language: str = "en",
        voice_type: str = "female"
    ) -> dict[str, Any]:
        """
        Generate video for a learning cycle.

        Args:
            session_id: Session identifier
            cycle_number: Cycle number (for filename)
            image_urls: List of image URLs/paths
            narratives: List of narrative texts for TTS
            language: Language code for TTS
            voice_type: Voice type (male/female)

        Returns:
            Dictionary with video URL and metadata

        Raises:
            Exception: If video generation fails
        """
        try:
            # Validate inputs
            if not image_urls or not narratives:
                raise ValueError("Images and narratives are required")

            if len(image_urls) != len(narratives):
                raise ValueError("Number of images must match number of narratives")

            # Get session details
            session = self.sessions_handler.find_one({"session_id": session_id})
            if not session:
                raise ValueError(f"Session {session_id} not found")

            user_id = session.get("user_id", "")
            topic = session.get("topic", "")

            # Generate audio for each narrative
            audio_files = []
            for i, narrative in enumerate(narratives):
                audio_file = await self._generate_audio(
                    text=narrative,
                    language=language,
                    voice_type=voice_type,
                    segment_id=f"{session_id}_cycle{cycle_number}_seg{i}"
                )
                if audio_file:
                    audio_files.append(audio_file)

            if not audio_files:
                raise Exception("Failed to generate audio files")

            # Convert image URLs to local paths
            image_paths = []
            for image_url in image_urls:
                # Remove /media/ prefix if present
                image_path = image_url.replace("/media/", "")
                full_path = settings.MEDIA_DIR / image_path
                if full_path.exists():
                    image_paths.append(str(full_path))

            if not image_paths:
                raise Exception("No valid image paths found")

            # Generate video using FFmpeg
            video_path = await self._create_video(
                session_id=session_id,
                cycle_number=cycle_number,
                image_paths=image_paths,
                audio_paths=audio_files
            )

            if not video_path:
                raise Exception("Failed to create video")

            # Save to learning history
            self._save_video_to_history(
                user_id=user_id,
                session_id=session_id,
                video_path=video_path,
                topic=topic,
                cycle_number=cycle_number
            )

            return {
                "session_id": session_id,
                "cycle_number": cycle_number,
                "video_url": video_path,
                "status": "ready",
                "duration_seconds": 8,
                "generated_at": datetime.now().isoformat()
            }

        except Exception as e:
            raise Exception(f"Failed to generate video: {str(e)}")

    async def _generate_audio(
        self,
        text: str,
        language: str,
        voice_type: str,
        segment_id: str
    ) -> Optional[str]:
        """
        Generate audio file from text using TTS.

        Args:
            text: Text to convert to speech
            language: Language code
            voice_type: Voice type
            segment_id: Segment identifier for filename

        Returns:
            Path to audio file or None if fails
        """
        try:
            # Generate audio using TTS provider
            audio_bytes = await self.tts_provider.synthesize_speech(
                text=text,
                language=language,
                voice_type=voice_type,
                speed=1.0
            )

            # Save audio file
            audio_filename = f"{segment_id}.mp3"
            audio_folder = settings.MEDIA_DIR / "audio"
            audio_folder.mkdir(parents=True, exist_ok=True)

            audio_path = audio_folder / audio_filename

            with open(audio_path, "wb") as f:
                f.write(audio_bytes)

            return str(audio_path)

        except Exception as e:
            print(f"Error generating audio: {e}")
            return None

    async def _create_video(
        self,
        session_id: str,
        cycle_number: int,
        image_paths: list[str],
        audio_paths: list[str]
    ) -> Optional[str]:
        """
        Create video from images and audio using FFmpeg.

        Args:
            session_id: Session identifier
            cycle_number: Cycle number
            image_paths: List of image file paths
            audio_paths: List of audio file paths

        Returns:
            Video URL or None if fails
        """
        try:
            # Calculate duration per image
            duration_per_image = 8.0 / len(image_paths)

            # Create temporary file list for FFmpeg
            temp_dir = settings.MEDIA_DIR / "temp"
            temp_dir.mkdir(parents=True, exist_ok=True)

            concat_file = temp_dir / f"{session_id}_cycle{cycle_number}_concat.txt"

            # Write concat file for images
            with open(concat_file, "w") as f:
                for image_path in image_paths:
                    f.write(f"file '{image_path}'\n")
                    f.write(f"duration {duration_per_image}\n")
                # Add last image again (FFmpeg requirement)
                f.write(f"file '{image_paths[-1]}'\n")

            # Concatenate audio files if multiple
            if len(audio_paths) > 1:
                audio_concat_file = temp_dir / f"{session_id}_cycle{cycle_number}_audio.txt"
                with open(audio_concat_file, "w") as f:
                    for audio_path in audio_paths:
                        f.write(f"file '{audio_path}'\n")

                combined_audio = temp_dir / f"{session_id}_cycle{cycle_number}_audio.mp3"

                # Combine audio files
                audio_cmd = [
                    "ffmpeg",
                    "-f", "concat",
                    "-safe", "0",
                    "-i", str(audio_concat_file),
                    "-c", "copy",
                    str(combined_audio),
                    "-y"
                ]

                result = subprocess.run(audio_cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Audio concat error: {result.stderr}")
                    audio_file = audio_paths[0]  # Fallback to first audio
                else:
                    audio_file = str(combined_audio)
            else:
                audio_file = audio_paths[0]

            # Create output video path
            output_filename = f"{session_id}_cycle{cycle_number}.mp4"
            output_path = settings.MEDIA_DIR / "generated_videos" / output_filename

            # Run FFmpeg to create video
            ffmpeg_cmd = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_file),
                "-i", audio_file,
                "-c:v", "libx264",
                "-tune", "stillimage",
                "-c:a", "aac",
                "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-shortest",
                "-t", "8",  # Limit to 8 seconds
                str(output_path),
                "-y"
            ]

            # Run FFmpeg with timeout
            result = await asyncio.create_subprocess_exec(
                *ffmpeg_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    result.communicate(),
                    timeout=settings.FFMPEG_TIMEOUT_SECONDS
                )
            except asyncio.TimeoutError:
                result.kill()
                await result.wait()
                print(f"FFmpeg timeout after {settings.FFMPEG_TIMEOUT_SECONDS} seconds")
                # Clean up on timeout
                concat_file.unlink(missing_ok=True)
                if len(audio_paths) > 1:
                    audio_concat_file.unlink(missing_ok=True)
                    if combined_audio.exists():
                        combined_audio.unlink(missing_ok=True)
                return None

            if result.returncode != 0:
                print(f"FFmpeg error: {stderr.decode()}")
                # Clean up on error
                concat_file.unlink(missing_ok=True)
                if len(audio_paths) > 1:
                    audio_concat_file.unlink(missing_ok=True)
                    if combined_audio.exists():
                        combined_audio.unlink(missing_ok=True)
                return None

            # Clean up temporary files after success
            concat_file.unlink(missing_ok=True)
            if len(audio_paths) > 1:
                audio_concat_file.unlink(missing_ok=True)
                if combined_audio.exists():
                    combined_audio.unlink(missing_ok=True)

            # Return relative URL
            return f"/media/generated_videos/{output_filename}"

        except Exception as e:
            print(f"Error creating video: {e}")
            # Clean up temporary files on any error
            try:
                if 'concat_file' in locals():
                    concat_file.unlink(missing_ok=True)
                if 'audio_concat_file' in locals():
                    audio_concat_file.unlink(missing_ok=True)
                if 'combined_audio' in locals() and combined_audio.exists():
                    combined_audio.unlink(missing_ok=True)
            except Exception as cleanup_error:
                print(f"Error during cleanup: {cleanup_error}")
            return None

    def _save_video_to_history(
        self,
        user_id: str,
        session_id: str,
        video_path: str,
        topic: str,
        cycle_number: int
    ) -> bool:
        """
        Save video to learning history.

        Args:
            user_id: User identifier
            session_id: Session identifier
            video_path: Path to video
            topic: Learning topic
            cycle_number: Cycle number

        Returns:
            Success status
        """
        try:
            history_id = self.history_handler.generate_id("HIS", "history_id")

            history_data = {
                "history_id": history_id,
                "user_id": user_id,
                "session_id": session_id,
                "content_type": "video",
                "content_id": f"{session_id}_cycle{cycle_number}",
                "content_path": video_path,
                "topic": topic,
                "viewed_at": datetime.now().isoformat()
            }

            return self.history_handler.append(history_data)

        except Exception as e:
            print(f"Error saving video to history: {e}")
            return False

    async def generate_cycle_video(
        self,
        session_id: str,
        cycle_number: int,
        user_id: str
    ) -> str:
        """
        Generate video for a learning cycle (API route wrapper).

        Args:
            session_id: Session identifier
            cycle_number: Cycle number
            user_id: User identifier

        Returns:
            Video URL

        Raises:
            Exception: If video generation fails
        """
        try:
            # Get session to retrieve images and narratives
            session = self.sessions_handler.find_one({"session_id": session_id})
            if not session:
                raise ValueError("Session not found")

            # Get learning history to find images for this session
            from app.database.csv_handler import get_learning_history_handler
            history_handler = get_learning_history_handler()
            all_history = history_handler.find_all({"session_id": session_id})

            # Filter images for this cycle
            image_records = [
                h for h in all_history
                if h.get("content_type") == "image"
            ]

            if not image_records:
                raise ValueError("No images found for this session")

            # Get image URLs and create default narratives if needed
            image_urls = [r.get("content_path", "") for r in image_records[:3]]
            narratives = [
                f"Learning about {session.get('topic', 'topic')}." for _ in image_urls
            ]

            # Generate video
            result = await self.generate_video_for_cycle(
                session_id=session_id,
                cycle_number=cycle_number,
                image_urls=image_urls,
                narratives=narratives,
                language="en",
                voice_type="female"
            )

            return result.get("video_url", "")

        except Exception as e:
            raise Exception(f"Failed to generate cycle video: {str(e)}")

    async def check_video_status(
        self,
        session_id: str,
        cycle_number: int
    ) -> dict[str, Any]:
        """
        Check if video exists for a session cycle.

        Args:
            session_id: Session identifier
            cycle_number: Cycle number

        Returns:
            Status dictionary
        """
        try:
            video_filename = f"{session_id}_cycle{cycle_number}.mp4"
            video_path = settings.MEDIA_DIR / "generated_videos" / video_filename

            if video_path.exists():
                return {
                    "session_id": session_id,
                    "cycle_number": cycle_number,
                    "status": "ready",
                    "video_url": f"/media/generated_videos/{video_filename}",
                    "size_bytes": video_path.stat().st_size
                }
            else:
                return {
                    "session_id": session_id,
                    "cycle_number": cycle_number,
                    "status": "not_found"
                }

        except Exception as e:
            return {
                "session_id": session_id,
                "cycle_number": cycle_number,
                "status": "error",
                "error": str(e)
            }

    async def regenerate_video(
        self,
        session_id: str,
        cycle_number: int
    ) -> dict[str, Any]:
        """
        Regenerate video for a cycle (admin function).

        Args:
            session_id: Session identifier
            cycle_number: Cycle number

        Returns:
            Generation result
        """
        try:
            # Get session to retrieve original data
            session = self.sessions_handler.find_one({"session_id": session_id})
            if not session:
                raise ValueError("Session not found")

            # This would need to retrieve the original images and narratives
            # For now, return a message that regeneration is not implemented
            return {
                "status": "not_implemented",
                "message": "Video regeneration requires original content data"
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    async def health_check(self) -> dict[str, Any]:
        """
        Check health of video generator service.

        Returns:
            Health status dictionary
        """
        try:
            # Check if FFmpeg is available
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True
            )

            ffmpeg_available = result.returncode == 0

            # Check TTS provider
            tts_healthy = await self.tts_provider.health_check()

            return {
                "service": "VideoGenerator",
                "status": "healthy" if (ffmpeg_available and tts_healthy) else "degraded",
                "ffmpeg": "available" if ffmpeg_available else "not_found",
                "tts_provider": "healthy" if tts_healthy else "unhealthy"
            }

        except Exception as e:
            return {
                "service": "VideoGenerator",
                "status": "unhealthy",
                "error": str(e)
            }
