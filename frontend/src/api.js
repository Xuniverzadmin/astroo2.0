const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function analyzeName(name) {
  const res = await fetch(`${API_URL}/analyze_name`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ name })
  });
  if (!res.ok) throw new Error("API error");
  return res.json();
}

export async function analyzeNameGet(name) {
  const res = await fetch(`${API_URL}/analyze_name/${encodeURIComponent(name)}`);
  if (!res.ok) throw new Error("API error");
  return res.json();
}

export async function checkHealth() {
  const res = await fetch(`${API_URL}/healthz`);
  if (!res.ok) throw new Error("Health check failed");
  return res.json();
}
