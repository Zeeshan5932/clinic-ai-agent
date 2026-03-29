const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const NORMALIZED_API_BASE_URL = API_BASE_URL.endsWith("/")
  ? API_BASE_URL.slice(0, -1)
  : API_BASE_URL;

function buildApiUrl(path) {
  return `${NORMALIZED_API_BASE_URL}${path}`;
}

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

  const response = await fetch(buildApiUrl("/api/v1/chat"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  return parseResponse(response);
}

export async function fetchHealthStatus() {
  const endpoints = ["/health", "/api/v1/health"];
  let lastError = null;

  for (const endpoint of endpoints) {
    try {
      const response = await fetch(buildApiUrl(endpoint));
      return await parseResponse(response);
    } catch (error) {
      lastError = error;
    }
  }

  throw lastError || new Error("Unable to fetch health status.");
}

export { API_BASE_URL };
