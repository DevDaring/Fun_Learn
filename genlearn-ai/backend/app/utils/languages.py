"""
Language constants for multi-language support.
Maps language codes to human-readable names.
"""

# Supported languages with their codes and names
SUPPORTED_LANGUAGES = {
    "en": "English",
    "zh": "Mandarin Chinese",
    "es": "Spanish",
    "hi": "Hindi",
    "pt": "Portuguese",
    "bn": "Bengali",
    "ru": "Russian",
    "ja": "Japanese",
    "pa": "Punjabi",
    "vi": "Vietnamese",
    "ar": "Arabic",
}

DEFAULT_LANGUAGE = "en"


def get_language_name(code: str) -> str:
    """Get the language name from a language code."""
    return SUPPORTED_LANGUAGES.get(code, "English")


def get_language_instruction(language: str) -> str:
    """
    Generate a strong language instruction for AI prompts.
    Ensures AI responds in the specified language.
    """
    if language == "en" or language not in SUPPORTED_LANGUAGES:
        return ""
    
    lang_name = SUPPORTED_LANGUAGES[language]
    return f"""
CRITICAL LANGUAGE REQUIREMENT: You MUST respond entirely in {lang_name}.
- Write ALL your responses in {lang_name} language
- Only keep technical terms, proper nouns, or brand names in their original form
- Do NOT respond in English unless specifically discussing English language concepts
- This instruction overrides all other language preferences
"""
