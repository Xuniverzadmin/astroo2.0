import { useState } from "react";
import { getMiniReading } from "../api";

export default function InstantMiniReading() {
  const [form, setForm] = useState({ 
    name: "", 
    dob: "", 
    tob: "", 
    location: "" 
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [summary, setSummary] = useState("");

  function onChange(key, value) {
    setForm(prev => ({ ...prev, [key]: value }));
  }

  async function run() {
    setError("");
    setSummary("");
    setLoading(true);
    try {
      const data = await getMiniReading(form);
      setSummary(data.summary || "");
    } catch (e) {
      setError(e.message || "Failed to generate mini reading");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <input 
          className="input input-bordered" 
          placeholder="Name" 
          value={form.name} 
          onChange={e => onChange("name", e.target.value)} 
        />
        <input 
          className="input input-bordered" 
          placeholder="DOB (YYYY-MM-DD)" 
          value={form.dob} 
          onChange={e => onChange("dob", e.target.value)} 
        />
        <input 
          className="input input-bordered" 
          placeholder="Time of Birth (HH:MM)" 
          value={form.tob} 
          onChange={e => onChange("tob", e.target.value)} 
        />
        <input 
          className="input input-bordered" 
          placeholder="Location" 
          value={form.location} 
          onChange={e => onChange("location", e.target.value)} 
        />
      </div>
      <button 
        className="btn btn-secondary" 
        disabled={loading || !form.name || !form.dob} 
        onClick={run}
      >
        {loading ? "Calculating..." : "Instant Mini Reading"}
      </button>
      {error && <div className="text-red-500 text-sm">{error}</div>}
      {summary && (
        <div className="p-3 bg-base-200 rounded whitespace-pre-wrap">
          {summary}
        </div>
      )}
    </div>
  );
}
