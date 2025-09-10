import { useState } from "react";
import { askAstrooverz } from "../api";

export default function AskAstrooverz() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState("");
  const [error, setError] = useState("");

  async function handleAsk() {
    setError("");
    setAnswer("");
    setLoading(true);
    try {
      const data = await askAstrooverz(question);
      setAnswer(data.answer || "");
    } catch (e) {
      setError(e.message || "Failed to ask");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-3">
      <textarea 
        value={question} 
        onChange={e => setQuestion(e.target.value)} 
        className="textarea textarea-bordered w-full" 
        placeholder="Ask Astrooverz anything..."
        rows={3}
      />
      <button 
        className="btn btn-primary" 
        disabled={loading || !question.trim()} 
        onClick={handleAsk}
      >
        {loading ? "Thinking..." : "Ask"}
      </button>
      {error && <div className="text-red-500 text-sm">{error}</div>}
      {answer && (
        <div className="p-3 bg-base-200 rounded whitespace-pre-wrap">
          {answer}
        </div>
      )}
    </div>
  );
}
