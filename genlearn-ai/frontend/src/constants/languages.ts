/**
 * Supported languages for multi-language chat feature.
 * Each language has a code, English name, and native name for display.
 */

export interface Language {
    code: string;
    name: string;
    nativeName: string;
}

export const SUPPORTED_LANGUAGES: Language[] = [
    { code: 'en', name: 'English', nativeName: 'English' },
    { code: 'zh', name: 'Mandarin Chinese', nativeName: '中文' },
    { code: 'es', name: 'Spanish', nativeName: 'Español' },
    { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी' },
    { code: 'pt', name: 'Portuguese', nativeName: 'Português' },
    { code: 'bn', name: 'Bengali', nativeName: 'বাংলা' },
    { code: 'ru', name: 'Russian', nativeName: 'Русский' },
    { code: 'ja', name: 'Japanese', nativeName: '日本語' },
    { code: 'pa', name: 'Punjabi', nativeName: 'ਪੰਜਾਬੀ' },
    { code: 'vi', name: 'Vietnamese', nativeName: 'Tiếng Việt' },
    { code: 'ar', name: 'Arabic', nativeName: 'العربية' },
];

export const DEFAULT_LANGUAGE = 'en';

export function getLanguageName(code: string): string {
    const lang = SUPPORTED_LANGUAGES.find((l) => l.code === code);
    return lang ? lang.name : 'English';
}

export function getLanguageNativeName(code: string): string {
    const lang = SUPPORTED_LANGUAGES.find((l) => l.code === code);
    return lang ? lang.nativeName : 'English';
}
