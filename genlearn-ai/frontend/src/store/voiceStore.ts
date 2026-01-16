import { create } from 'zustand';

interface VoiceStore {
  isRecording: boolean;
  isPlaying: boolean;
  isSpeaking: boolean;
  audioBlob: Blob | null;
  transcript: string;
  error: string | null;

  setRecording: (recording: boolean) => void;
  setPlaying: (playing: boolean) => void;
  setSpeaking: (speaking: boolean) => void;
  setAudioBlob: (blob: Blob | null) => void;
  setTranscript: (transcript: string) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

export const useVoiceStore = create<VoiceStore>((set) => ({
  isRecording: false,
  isPlaying: false,
  isSpeaking: false,
  audioBlob: null,
  transcript: '',
  error: null,

  setRecording: (recording) => set({ isRecording: recording }),
  setPlaying: (playing) => set({ isPlaying: playing }),
  setSpeaking: (speaking) => set({ isSpeaking: speaking }),
  setAudioBlob: (blob) => set({ audioBlob: blob }),
  setTranscript: (transcript) => set({ transcript }),
  setError: (error) => set({ error }),
  reset: () => set({
    isRecording: false,
    isPlaying: false,
    isSpeaking: false,
    audioBlob: null,
    transcript: '',
    error: null,
  }),
}));
