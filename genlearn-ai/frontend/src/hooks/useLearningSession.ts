import { useState, useCallback } from 'react';
import { useLearningStore } from '../store/learningStore';
import api from '../services/api';
import { CourseConfig } from '../types';

export const useLearningSession = () => {
  const {
    currentSession,
    content,
    currentCycle,
    isLoading,
    error,
    setSession,
    setContent,
    setCurrentCycle,
    setLoading,
    setError,
    clearSession,
  } = useLearningStore();

  const [videoStatus, setVideoStatus] = useState<any>(null);

  const startNewSession = useCallback(async (config: CourseConfig) => {
    setLoading(true);
    setError(null);

    try {
      const session = await api.startSession(config);
      setSession(session);

      // Load content
      const sessionContent = await api.getSessionContent(session.session_id);
      setContent(sessionContent);
      setCurrentCycle(1);

      setLoading(false);
      return session;
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to start session');
      setLoading(false);
      throw err;
    }
  }, [setSession, setContent, setCurrentCycle, setLoading, setError]);

  const progressToCycle = useCallback(async (cycleNumber: number) => {
    if (!currentSession) return;

    setCurrentCycle(cycleNumber);

    // Submit progress
    try {
      await api.submitProgress(currentSession.session_id, {
        current_cycle: cycleNumber,
      });
    } catch (err) {
      console.error('Failed to submit progress:', err);
    }
  }, [currentSession, setCurrentCycle]);

  const endCurrentSession = useCallback(async (finalScore: number = 0, completed: boolean = true) => {
    if (!currentSession) return;

    try {
      await api.endSession(currentSession.session_id, finalScore, 0, completed);
      clearSession();
    } catch (err) {
      console.error('Failed to end session:', err);
    }
  }, [currentSession, clearSession]);

  const checkVideoGeneration = useCallback(async (cycleNumber: number) => {
    if (!currentSession) return;

    try {
      const status = await api.checkVideoStatus(currentSession.session_id, cycleNumber);
      setVideoStatus(status);
      return status;
    } catch (err) {
      console.error('Failed to check video status:', err);
    }
  }, [currentSession]);

  return {
    currentSession,
    content,
    currentCycle,
    isLoading,
    error,
    videoStatus,
    startNewSession,
    progressToCycle,
    endCurrentSession,
    checkVideoGeneration,
  };
};
