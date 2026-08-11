import axios from 'axios';

// FastAPI backend
const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Scan a URL
export const scanUrl = async (url) => {
  try {
    const response = await api.post('/scan/', { url });
    return response.data;
  } catch (error) {
    console.error('API Error during URL scan:', error);
    throw error;
  }
};

// Get scan history
export const getHistory = async () => {
  try {
    const response = await api.get('/history/');
    return response.data;
  } catch (error) {
    console.error('API Error while getting history:', error);
    throw error;
  }
};

// Delete one scan
export const deleteHistory = async (scanId) => {
  try {
    const response = await api.delete(`/history/${scanId}`);
    return response.data;
  } catch (error) {
    console.error('API Error while deleting scan:', error);
    throw error;
  }
};

// Delete all history
export const clearHistory = async () => {
  try {
    const response = await api.delete('/history/');
    return response.data;
  } catch (error) {
    console.error('API Error while clearing history:', error);
    throw error;
  }
};

export default api;

