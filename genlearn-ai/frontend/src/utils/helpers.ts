/**
 * Helper utility functions
 */

/**
 * Calculate user level based on XP points
 */
export const calculateLevel = (xpPoints: number): number => {
  return Math.floor(xpPoints / 500) + 1;
};

/**
 * Calculate XP needed for next level
 */
export const xpForNextLevel = (currentXP: number): number => {
  const currentLevel = calculateLevel(currentXP);
  return currentLevel * 500 - currentXP;
};

/**
 * Format date to readable string
 */
export const formatDate = (date: string | Date): string => {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

/**
 * Format time to readable string
 */
export const formatTime = (date: string | Date): string => {
  const d = typeof date === 'string' ? new Date(date) : date;
  return d.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
  });
};

/**
 * Format duration in minutes to readable string
 */
export const formatDuration = (minutes: number): string => {
  if (minutes < 60) {
    return `${minutes}m`;
  }
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return mins > 0 ? `${hours}h ${mins}m` : `${hours}h`;
};

/**
 * Get difficulty color based on level
 */
export const getDifficultyColor = (level: number): string => {
  if (level <= 3) return 'text-green-600 bg-green-100';
  if (level <= 6) return 'text-yellow-600 bg-yellow-100';
  if (level <= 8) return 'text-orange-600 bg-orange-100';
  return 'text-red-600 bg-red-100';
};

/**
 * Get status color
 */
export const getStatusColor = (status: string): string => {
  switch (status) {
    case 'active':
    case 'in_progress':
    case 'completed':
      return 'text-green-600 bg-green-100';
    case 'upcoming':
      return 'text-blue-600 bg-blue-100';
    case 'abandoned':
    case 'failed':
      return 'text-red-600 bg-red-100';
    default:
      return 'text-gray-600 bg-gray-100';
  }
};

/**
 * Truncate text to specified length
 */
export const truncate = (text: string, length: number): string => {
  if (text.length <= length) return text;
  return text.substring(0, length) + '...';
};

/**
 * Convert blob to base64
 */
export const blobToBase64 = (blob: Blob): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result as string);
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
};

/**
 * Play audio from blob
 */
export const playAudio = (audioBlob: Blob): Promise<void> => {
  return new Promise((resolve, reject) => {
    const audio = new Audio(URL.createObjectURL(audioBlob));
    audio.onended = () => resolve();
    audio.onerror = reject;
    audio.play();
  });
};

/**
 * Calculate time remaining
 */
export const timeRemaining = (endDate: string): string => {
  const now = new Date();
  const end = new Date(endDate);
  const diff = end.getTime() - now.getTime();

  if (diff < 0) return 'Ended';

  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

  if (days > 0) return `${days}d ${hours}h`;
  if (hours > 0) return `${hours}h ${minutes}m`;
  return `${minutes}m`;
};

/**
 * Debounce function
 */
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  wait: number
): ((...args: Parameters<T>) => void) => {
  let timeout: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
};

export const cn = (...classes: (string | boolean | undefined)[]): string => {
  return classes.filter(Boolean).join(' ');
};

/**
 * Format chat content with proper markdown rendering
 * Handles: bold, italic, bullet points, numbered lists, LaTeX math, code blocks
 */
export const formatChatContent = (content: string): string => {
  let formatted = content
    // Escape HTML to prevent XSS
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')

    // Code blocks (```)
    .replace(/```(\w*)\n?([\s\S]*?)```/g, '<pre class="bg-gray-800 text-green-400 p-3 rounded-lg my-2 overflow-x-auto text-sm"><code>$2</code></pre>')

    // Inline code (`)
    .replace(/`([^`]+)`/g, '<code class="bg-gray-200 text-red-600 px-1 rounded text-sm">$1</code>')

    // LaTeX math - inline $...$ -> styled span
    .replace(/\$([^$]+)\$/g, '<span class="font-mono text-blue-600 bg-blue-50 px-1 rounded">$1</span>')

    // Bold **text**
    .replace(/\*\*([^*]+)\*\*/g, '<strong class="font-semibold">$1</strong>')

    // Italic *text* (but not bullet points at line start)
    .replace(/(?<!^|\n)\*([^*\n]+)\*/g, '<em>$1</em>')

    // Bullet points: * at start of line
    .replace(/^[\*\-]\s+(.+)$/gm, '<li class="ml-4 list-disc">$1</li>')

    // Numbered lists: 1. at start of line
    .replace(/^\d+\.\s+(.+)$/gm, '<li class="ml-4 list-decimal">$1</li>')

    // Wrap consecutive list items in ul/ol
    .replace(/((?:<li class="ml-4 list-disc">.*<\/li>\n?)+)/g, '<ul class="my-2 space-y-1">$1</ul>')
    .replace(/((?:<li class="ml-4 list-decimal">.*<\/li>\n?)+)/g, '<ol class="my-2 space-y-1">$1</ol>')

    // Headers (### Header)
    .replace(/^###\s+(.+)$/gm, '<h3 class="font-bold text-lg mt-3 mb-1">$1</h3>')
    .replace(/^##\s+(.+)$/gm, '<h2 class="font-bold text-xl mt-4 mb-2">$1</h2>')
    .replace(/^#\s+(.+)$/gm, '<h1 class="font-bold text-2xl mt-4 mb-2">$1</h1>')

    // Line breaks
    .replace(/\n\n/g, '</p><p class="mb-2">')
    .replace(/\n/g, '<br/>');

  // Wrap in paragraph
  return '<p class="mb-2">' + formatted + '</p>';
};
