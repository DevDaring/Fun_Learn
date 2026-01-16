"""
File Handler
Manages file uploads and storage
"""

import os
import uuid
from pathlib import Path
from typing import Optional
from datetime import datetime
import shutil
from app.config import settings


class FileHandler:
    """Handles file operations for media storage"""

    @staticmethod
    def generate_filename(original_filename: str, prefix: str = "") -> str:
        """
        Generate unique filename

        Args:
            original_filename: Original file name
            prefix: Optional prefix for the filename

        Returns:
            Unique filename with timestamp
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_str = uuid.uuid4().hex[:8]
        extension = Path(original_filename).suffix
        if prefix:
            return f"{prefix}_{timestamp}_{random_str}{extension}"
        return f"{timestamp}_{random_str}{extension}"

    @staticmethod
    def save_file(file_data: bytes, filename: str, subfolder: str) -> tuple[bool, str]:
        """
        Save file to media folder

        Args:
            file_data: File bytes
            filename: Filename
            subfolder: Subfolder in media directory (e.g., 'avatars', 'characters')

        Returns:
            Tuple of (success, file_path)
        """
        try:
            folder_path = settings.MEDIA_DIR / subfolder
            folder_path.mkdir(parents=True, exist_ok=True)

            file_path = folder_path / filename
            with open(file_path, 'wb') as f:
                f.write(file_data)

            # Return relative path from media dir
            relative_path = f"{subfolder}/{filename}"
            return True, relative_path
        except Exception as e:
            print(f"Error saving file: {e}")
            return False, ""

    @staticmethod
    def get_file_url(file_path: str) -> str:
        """
        Get public URL for file

        Args:
            file_path: Relative path from media directory

        Returns:
            Full URL to access the file
        """
        return f"/media/{file_path}"

    @staticmethod
    def delete_file(file_path: str) -> bool:
        """
        Delete file from storage

        Args:
            file_path: Relative path from media directory

        Returns:
            Success status
        """
        try:
            full_path = settings.MEDIA_DIR / file_path
            if full_path.exists():
                os.remove(full_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if file exists"""
        full_path = settings.MEDIA_DIR / file_path
        return full_path.exists()

    @staticmethod
    def get_file_path(file_path: str) -> Path:
        """Get full system path for file"""
        return settings.MEDIA_DIR / file_path

    @staticmethod
    def validate_file_type(filename: str, allowed_extensions: list) -> bool:
        """
        Validate file extension

        Args:
            filename: File name
            allowed_extensions: List of allowed extensions (e.g., ['.jpg', '.png'])

        Returns:
            True if valid
        """
        extension = Path(filename).suffix.lower()
        return extension in allowed_extensions

    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes"""
        try:
            full_path = settings.MEDIA_DIR / file_path
            return full_path.stat().st_size
        except Exception:
            return 0

    @staticmethod
    def copy_file(source_path: str, dest_subfolder: str, new_filename: Optional[str] = None) -> tuple[bool, str]:
        """
        Copy file to new location

        Args:
            source_path: Source file path (relative to media dir)
            dest_subfolder: Destination subfolder
            new_filename: Optional new filename

        Returns:
            Tuple of (success, new_file_path)
        """
        try:
            source_full = settings.MEDIA_DIR / source_path
            if not source_full.exists():
                return False, ""

            if not new_filename:
                new_filename = Path(source_path).name

            dest_folder = settings.MEDIA_DIR / dest_subfolder
            dest_folder.mkdir(parents=True, exist_ok=True)
            dest_full = dest_folder / new_filename

            shutil.copy2(source_full, dest_full)

            relative_path = f"{dest_subfolder}/{new_filename}"
            return True, relative_path
        except Exception as e:
            print(f"Error copying file: {e}")
            return False, ""

    @staticmethod
    def save_image(image_data: bytes, subfolder: str, filename: str) -> str:
        """
        Save image data to file
        
        Args:
            image_data: Raw image bytes
            subfolder: Subfolder to save in (e.g., 'avatars', 'characters')
            filename: Name of the file
            
        Returns:
            Relative path to saved file
            
        Raises:
            Exception if save fails
        """
        success, file_path = FileHandler.save_file(image_data, filename, subfolder)
        if not success:
            raise Exception(f"Failed to save image to {subfolder}/{filename}")
        return file_path


# Helper functions for specific file types
def save_avatar(file_data: bytes, user_id: str, extension: str = ".png") -> tuple[bool, str]:
    """Save avatar image"""
    filename = FileHandler.generate_filename(f"avatar_{user_id}{extension}", "avatar")
    return FileHandler.save_file(file_data, filename, "avatars")


def save_character(file_data: bytes, character_id: str, extension: str = ".png") -> tuple[bool, str]:
    """Save character image"""
    filename = FileHandler.generate_filename(f"character_{character_id}{extension}", "char")
    return FileHandler.save_file(file_data, filename, "characters")


def save_generated_image(file_data: bytes, session_id: str, segment_number: int) -> tuple[bool, str]:
    """Save generated learning image"""
    filename = f"{session_id}_seg{segment_number}.png"
    return FileHandler.save_file(file_data, filename, "generated_images")


def save_generated_video(file_data: bytes, session_id: str, cycle_number: int) -> tuple[bool, str]:
    """Save generated video"""
    filename = f"{session_id}_cycle{cycle_number}.mp4"
    return FileHandler.save_file(file_data, filename, "generated_videos")


def save_audio(file_data: bytes, audio_id: str, extension: str = ".mp3") -> tuple[bool, str]:
    """Save audio file"""
    filename = FileHandler.generate_filename(f"audio_{audio_id}{extension}", "audio")
    return FileHandler.save_file(file_data, filename, "audio")


def save_upload(file_data: bytes, original_filename: str) -> tuple[bool, str]:
    """Save uploaded file"""
    filename = FileHandler.generate_filename(original_filename, "upload")
    return FileHandler.save_file(file_data, filename, "uploads")
