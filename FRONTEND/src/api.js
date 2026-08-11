// API helper module for connecting Frontend with FastAPI Backend

const API_BASE_URL = "http://127.0.0.1:8000";

/**
 * Sends target URL to FastAPI backend for phishing threat analysis.
 * @param {string} url - The URL to scan
 * @returns {Promise<Object>} API JSON response data
 */
export async function scanUrl(url) {
  try {
    const response = await fetch(`${API_BASE_URL}/scan`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      throw new Error(`Server returned error status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("API Scan Error:", error);
    throw error;
  }
}