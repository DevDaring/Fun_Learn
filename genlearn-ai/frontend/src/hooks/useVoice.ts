import { useState, useCallback, useRef } from 'react';
import { useVoiceStore } from '../store/voiceStore';
import { useSettingsStore } from '../store/settingsStore';
import api from '../services/api';

export const useVoice = () => {
  const { language, voiceType, voiceSpeed } = useSettingsStore();
  const { setRecording, setAudioBlob, setTranscript, setError, setSpeaking, setPlaying } = useVoiceStore();
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      audioChunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        setAudioBlob(audioBlob);

        // Transcribe audio
        try {
          const result = await api.speechToText(audioBlob, language);
          setTranscript(result.text);
        } catch (error) {
          setError('Failed to transcribe audio');
        }

        stream.getTracks().forEach(track => track.stop());
      };

      recorder.start();
      setMediaRecorder(recorder);
      setRecording(true);
      setError(null);
    } catch (error) {
      setError('Failed to start recording. Please check microphone permissions.');
    }
  }, [language, setRecording, setAudioBlob, setTranscript, setError]);

  const stopRecording = useCallback(() => {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
      setRecording(false);
    }
  }, [mediaRecorder, setRecording]);

  const speakText = useCallback(async (text: string) => {
    try {
      setSpeaking(true);
      const audioBlob = await api.textToSpeech(text, language, voiceType);
      const audio = new Audio(URL.createObjectURL(audioBlob));
      audio.playbackRate = voiceSpeed;

      audio.onended = () => {
        setSpeaking(false);
      };

      audio.onerror = () => {
        setSpeaking(false);
        setError('Failed to play audio');
      };

      await audio.play();
    } catch (error) {
      setSpeaking(false);
      setError('Failed to generate speech');
    }
  }, [language, voiceType, voiceSpeed, setSpeaking, setError]);

  const playAudio = useCallback((audioUrl: string) => {
    return new Promise<void>((resolve, reject) => {
      setPlaying(true);
      const audio = new Audio(audioUrl);
      audio.playbackRate = voiceSpeed;

      audio.onended = () => {
        setPlaying(false);
        resolve();
      };

      audio.onerror = () => {
        setPlaying(false);
        setError('Failed to play audio');
        reject();
      };

      audio.play();
    });
  }, [voiceSpeed, setPlaying, setError]);

  return {
    startRecording,
    stopRecording,
    speakText,
    playAudio,
  };
};
