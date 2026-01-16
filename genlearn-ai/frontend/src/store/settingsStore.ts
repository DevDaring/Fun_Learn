import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface SettingsStore {
  language: string;
  voiceType: 'male' | 'female';
  voiceSpeed: number;
  fullVocalMode: boolean;
  theme: 'light' | 'dark';

  setLanguage: (language: string) => void;
  setVoiceType: (voiceType: 'male' | 'female') => void;
  setVoiceSpeed: (speed: number) => void;
  toggleFullVocalMode: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
}

export const useSettingsStore = create<SettingsStore>()(
  persist(
    (set) => ({
      language: 'en',
      voiceType: 'female',
      voiceSpeed: 1.0,
      fullVocalMode: false,
      theme: 'light',

      setLanguage: (language) => set({ language }),
      setVoiceType: (voiceType) => set({ voiceType }),
      setVoiceSpeed: (speed) => set({ voiceSpeed: speed }),
      toggleFullVocalMode: () => set((state) => ({ fullVocalMode: !state.fullVocalMode })),
      setTheme: (theme) => set({ theme }),
    }),
    {
      name: 'genlearn-settings',
    }
  )
);
