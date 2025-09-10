const API_BASE = import.meta.env.VITE_API_BASE || "/api";

export async function analyzeName(name) {
  const res = await fetch(`${API_BASE}/analyze_name`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ name })
  });
  if (!res.ok) throw new Error("API error");
  return res.json();
}

export async function analyzeNameGet(name) {
  const res = await fetch(`${API_BASE}/analyze_name/${encodeURIComponent(name)}`);
  if (!res.ok) throw new Error("API error");
  return res.json();
}

export async function checkHealth() {
  const res = await fetch(`${API_BASE}/healthz`);
  if (!res.ok) throw new Error("Health check failed");
  return res.json();
}
