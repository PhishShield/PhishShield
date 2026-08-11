const API_URL = "http://127.0.0.1:8000";

export async function checkBackendHealth() {
  try {
    const response = await fetch(`${API_URL}/health/`);

    if (!response.ok) {
      return false;
    }

    return true;
  } catch (error) {
    return false;
  }
}