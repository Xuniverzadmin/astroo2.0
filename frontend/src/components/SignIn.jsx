import { useState } from "react";
import { login } from "../api";

export default function SignIn({ onSuccess }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await login(email, password);
      localStorage.setItem("astro_token", data.access_token);
      onSuccess?.(data);
    } catch (err) {
      setError(err.message || "Sign in failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <input 
        value={email} 
        onChange={e=>setEmail(e.target.value)} 
        placeholder="Email" 
        className="input input-bordered w-full" 
        type="email"
        required
      />
      <input 
        type="password" 
        value={password} 
        onChange={e=>setPassword(e.target.value)} 
        placeholder="Password" 
        className="input input-bordered w-full"
        required
      />
      {error && <div className="text-red-500 text-sm">{error}</div>}
      <button disabled={loading} className="btn btn-primary w-full">
        {loading ? "Signing in..." : "Sign In"}
      </button>
    </form>
  );
}
