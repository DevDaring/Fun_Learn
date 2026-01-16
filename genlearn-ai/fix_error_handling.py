"""
Script to fix error handling across all route files
Replaces information-leaking error messages with safe generic messages
"""

import re
from pathlib import Path

# Define route files to fix
ROUTE_FILES = [
    "backend/app/api/routes/learning.py",
    "backend/app/api/routes/quiz.py",
    "backend/app/api/routes/avatar.py",
    "backend/app/api/routes/characters.py",
    "backend/app/api/routes/voice.py",
    "backend/app/api/routes/video.py",
    "backend/app/api/routes/teams.py",
    "backend/app/api/routes/tournaments.py",
    "backend/app/api/routes/admin.py",
    "backend/app/api/routes/users.py",
    "backend/app/api/routes/chat.py",
]

# Map of operation patterns to safe error messages
ERROR_MESSAGE_MAP = {
    "starting session": "SESSION_ERROR",
    "generating content": "CONTENT_GENERATION_ERROR",
    "updating progress": "SESSION_ERROR",
    "ending session": "SESSION_ERROR",
    "fetching MCQ questions": "QUESTION_ERROR",
    "submitting MCQ answer": "ANSWER_ERROR",
    "fetching descriptive questions": "QUESTION_ERROR",
    "submitting descriptive answer": "ANSWER_ERROR",
    "fetching avatars": "INTERNAL_ERROR",
    "creating avatar": "UPLOAD_ERROR",
    "deleting avatar": "INTERNAL_ERROR",
    "fetching characters": "INTERNAL_ERROR",
    "creating character": "UPLOAD_ERROR",
    "deleting character": "INTERNAL_ERROR",
    "generating speech": "INTERNAL_ERROR",
    "transcribing audio": "INTERNAL_ERROR",
    "fetching video": "VIDEO_ERROR",
    "checking video status": "VIDEO_ERROR",
    "fetching teams": "TEAM_ERROR",
    "creating team": "TEAM_ERROR",
    "joining team": "TEAM_ERROR",
    "fetching tournaments": "TOURNAMENT_ERROR",
    "joining tournament": "TOURNAMENT_ERROR",
    "fetching leaderboard": "TOURNAMENT_ERROR",
    "creating tournament": "TOURNAMENT_ERROR",
    "uploading questions": "UPLOAD_ERROR",
    "fetching users": "INTERNAL_ERROR",
    "fetching profile": "INTERNAL_ERROR",
    "updating profile": "INTERNAL_ERROR",
    "fetching learning history": "INTERNAL_ERROR",
    "updating settings": "INTERNAL_ERROR",
    "processing chat message": "INTERNAL_ERROR",
}


def add_imports(content: str) -> str:
    """Add error handler imports if not present"""
    if "from app.utils.error_handler import" in content:
        return content

    # Find where to insert imports (after existing imports)
    import_pattern = r'(from app\.utils\.helpers import [^\n]+\n)'
    if re.search(import_pattern, content):
        content = re.sub(
            import_pattern,
            r'\1from app.utils.error_handler import handle_error, ErrorMessages\n',
            content
        )
    else:
        # Add after router import
        router_pattern = r'(from app\.api\.dependencies import [^\n]+\n)'
        if re.search(router_pattern, content):
            content = re.sub(
                router_pattern,
                r'\1from app.utils.error_handler import handle_error, ErrorMessages\n',
                content
            )

    # Add logging import if not present
    if "import logging" not in content:
        content = re.sub(
            r'("""[^"]+""")\n\n',
            r'\1\n\nimport logging\n',
            content,
            count=1
        )

    # Add logger if not present
    if "logger = logging.getLogger(__name__)" not in content:
        content = re.sub(
            r'(router = APIRouter\(\))',
            r'logger = logging.getLogger(__name__)\n\1',
            content
        )

    return content


def fix_error_handling(content: str, operation: str, error_msg: str) -> str:
    """Fix a specific error handling pattern"""
    # Pattern to match the old error format
    old_pattern = rf'detail=f"Error {operation}: {{str\(e\)}}"'

    # New pattern with safe error handling
    new_pattern = f'public_message=ErrorMessages.{error_msg}'

    # Replace in except blocks
    # Pattern: except Exception as e: raise HTTPException(...detail=f"Error...")
    full_old_pattern = (
        r'except Exception as e:\s*'
        r'raise HTTPException\(\s*'
        r'status_code=status\.[A-Z_0-9]+,\s*'
        rf'detail=f"Error {re.escape(operation)}: {{str\(e\)}}"\s*'
        r'\)'
    )

    full_new_pattern = (
        r'except HTTPException:\n        raise\n    '
        r'except Exception as e:\n        '
        r'raise handle_error(\n            e,\n            '
        rf'"{operation}",\n            '
        f'public_message=ErrorMessages.{error_msg}\n        '
        r')'
    )

    content = re.sub(full_old_pattern, full_new_pattern, content, flags=re.MULTILINE)

    return content


def process_file(file_path: Path):
    """Process a single route file"""
    if not file_path.exists():
        print(f"⚠️  File not found: {file_path}")
        return False

    print(f"📝 Processing: {file_path}")

    # Read file
    content = file_path.read_text(encoding='utf-8')

    # Add imports
    content = add_imports(content)

    # Fix all error handling patterns
    for operation, error_msg in ERROR_MESSAGE_MAP.items():
        content = fix_error_handling(content, operation, error_msg)

    # Write back
    file_path.write_text(content, encoding='utf-8')

    print(f"✅ Fixed: {file_path}")
    return True


def main():
    """Main function to fix all routes"""
    print("=" * 60)
    print("🔧 Fixing Error Handling in Routes")
    print("=" * 60)

    base_dir = Path(__file__).parent
    fixed = 0
    failed = 0

    for route_file in ROUTE_FILES:
        file_path = base_dir / route_file
        if process_file(file_path):
            fixed += 1
        else:
            failed += 1

    print("=" * 60)
    print(f"✅ Fixed: {fixed} files")
    if failed > 0:
        print(f"❌ Failed: {failed} files")
    print("=" * 60)


if __name__ == "__main__":
    main()
