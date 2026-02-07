/**
 * Global Language Context
 * Provides language state to all components across the application.
 * Persists language preference to user settings.
 */

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import api from '../services/api';
import { SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE } from '../constants/languages';

interface LanguageContextType {
    selectedLanguage: string;
    setLanguage: (code: string) => Promise<void>;
    languageName: string;
    isLoading: boolean;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

interface LanguageProviderProps {
    children: ReactNode;
}

export const LanguageProvider: React.FC<LanguageProviderProps> = ({ children }) => {
    const [selectedLanguage, setSelectedLanguage] = useState(DEFAULT_LANGUAGE);
    const [isLoading, setIsLoading] = useState(true);

    // Load user's language preference on mount
    useEffect(() => {
        const loadLanguagePreference = async () => {
            try {
                const user = await api.getCurrentUser();
                if (user?.language_preference) {
                    setSelectedLanguage(user.language_preference);
                }
            } catch (error) {
                // Use default language if not logged in or error
                console.log('Using default language');
            } finally {
                setIsLoading(false);
            }
        };
        loadLanguagePreference();
    }, []);

    const setLanguage = async (code: string) => {
        setSelectedLanguage(code);

        // Persist to backend
        try {
            await api.updateSettings({ language_preference: code });
        } catch (error) {
            console.log('Could not save language preference');
        }
    };

    const languageName = SUPPORTED_LANGUAGES.find(l => l.code === selectedLanguage)?.name || 'English';

    return (
        <LanguageContext.Provider value={{ selectedLanguage, setLanguage, languageName, isLoading }}>
            {children}
        </LanguageContext.Provider>
    );
};

export const useLanguage = (): LanguageContextType => {
    const context = useContext(LanguageContext);
    if (context === undefined) {
        throw new Error('useLanguage must be used within a LanguageProvider');
    }
    return context;
};
