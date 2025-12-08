/**
 * Analysis service for text analysis API calls.
 */
import api from './api';

export const analysisService = {
  /**
   * Analyze text using the backend API
   */
  async analyzeText(text, candidateLabels = null) {
    const payload = { text };
    
    if (candidateLabels && candidateLabels.length > 0) {
      payload.candidate_labels = candidateLabels;
    }

    const response = await api.post('/analyze', payload);
    return response.data;
  },
};
