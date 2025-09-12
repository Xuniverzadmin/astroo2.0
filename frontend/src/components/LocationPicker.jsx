import { useEffect, useRef, useState } from "react";

const NOMINATIM = "https://nominatim.openstreetmap.org/search";

export default function LocationPicker({ value, onSelect }) {
  const [q, setQ] = useState("");
  const [results, setResults] = useState([]);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const abortRef = useRef();

  // Debounced search
  useEffect(() => {
    if (!q || q.trim().length < 3) { setResults([]); return; }
    const tid = setTimeout(async () => {
      try {
        if (abortRef.current) abortRef.current.abort();
        abortRef.current = new AbortController();
        setLoading(true);
        const url = `${NOMINATIM}?q=${encodeURIComponent(q)}&format=json&addressdetails=1&limit=5`;
        const res = await fetch(url, {
          headers: { "Accept": "application/json" },
          signal: abortRef.current.signal
        });
        const data = await res.json();
        setResults((data || []).map(item => ({
          label: item.display_name,
          lat: parseFloat(item.lat),
          lon: parseFloat(item.lon),
        })));
      } catch (_) {
        // ignore
      } finally {
        setLoading(false);
        setOpen(true);
      }
    }, 350);
    return () => clearTimeout(tid);
  }, [q]);

  function choose(r) {
    onSelect?.(r);
    setQ("");
    setResults([]);
    setOpen(false);
  }

  return (
    <div className="relative">
      <div className="flex items-center gap-2">
        <input
          className="w-full bg-slate-800 text-white rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          placeholder="Search city or place (min 3 chars)"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onFocus={() => q.length >= 3 && setOpen(true)}
        />
        {loading && <span className="text-sm opacity-70">Searching…</span>}
      </div>

      {open && results.length > 0 && (
        <ul className="absolute z-50 mt-2 w-full max-h-60 overflow-auto rounded-md border border-slate-700 bg-slate-900 text-slate-100 shadow-lg">
          {results.map((r, i) => (
            <li
              key={i}
              className="px-3 py-2 cursor-pointer hover:bg-slate-800"
              onMouseDown={() => choose(r)}
            >
              {r.label}
            </li>
          ))}
        </ul>
      )}

      {value && (
        <p className="text-xs mt-2 opacity-70">
          Current: <b>{value.label}</b> ({value.lat.toFixed(3)}, {value.lon.toFixed(3)})
        </p>
      )}
    </div>
  );
}
