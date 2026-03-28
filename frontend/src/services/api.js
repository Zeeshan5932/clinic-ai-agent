const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function parseResponse(response) {
  const contentType = response.headers.get("content-type") || "";
  const body = contentType.includes("application/json")
    ? await response.json()
    : { response: await response.text() };

  if (!response.ok) {
    const detail = body?.detail || body?.message || "Something went wrong.";
    throw new Error(detail);
  }

  return body;
}

export async function sendChatMessage(message) {
  const payload = { message };

  // Prefer /chat per requirement, then fallback to /api/v1/chat for newer backend routes.
  const endpoints = ["/chat", "/api/v1/chat"];
  let lastError = null;

  for (const endpoint of endpoints) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      return await parseResponse(response);
    } catch (error) {
      lastError = error;
    }
  }

  throw lastError || new Error("Unable to reach backend API.");
}

export async function fetchHealthStatus() {
  const endpoints = ["/health", "/api/v1/health"];
  let lastError = null;

  for (const endpoint of endpoints) {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`);
      return await parseResponse(response);
    } catch (error) {
      lastError = error;
    }
  }

  throw lastError || new Error("Unable to fetch health status.");
}

export { API_BASE_URL };
