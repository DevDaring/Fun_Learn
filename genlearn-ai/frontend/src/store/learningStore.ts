import { create } from 'zustand';
import { LearningSession, LearningContent } from '../types';

interface LearningStore {
  currentSession: LearningSession | null;
  content: LearningContent | null;
  currentCycle: number;
  isLoading: boolean;
  error: string | null;

  setSession: (session: LearningSession) => void;
  setContent: (content: LearningContent) => void;
  setCurrentCycle: (cycle: number) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearSession: () => void;
}

export const useLearningStore = create<LearningStore>((set) => ({
  currentSession: null,
  content: null,
  currentCycle: 0,
  isLoading: false,
  error: null,

  setSession: (session) => set({ currentSession: session }),
  setContent: (content) => set({ content }),
  setCurrentCycle: (cycle) => set({ currentCycle: cycle }),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
  clearSession: () => set({
    currentSession: null,
    content: null,
    currentCycle: 0,
    isLoading: false,
    error: null,
  }),
}));
