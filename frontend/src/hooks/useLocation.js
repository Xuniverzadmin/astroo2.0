import { useEffect, useState } from "react";

// Default fallback (Chennai)
const DEFAULT_LOC = { lat: 13.0827, lon: 80.2707, label: "Chennai, India" };
const LS_KEY = "astrooverz_location";

export function useLocation() {
  const [location, setLocation] = useState(() => {
    const saved = localStorage.getItem(LS_KEY);
    return saved ? JSON.parse(saved) : DEFAULT_LOC;
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const saved = localStorage.getItem(LS_KEY);
    if (saved) { setLoading(false); return; } // user preference overrides auto-detect

    async function detect() {
      try {
        if ("geolocation" in navigator) {
          navigator.geolocation.getCurrentPosition(
            (pos) => {
              setLocation({
                lat: pos.coords.latitude,
                lon: pos.coords.longitude,
                label: "My Current Location",
              });
              setLoading(false);
            },
            async () => {
              try {
                const res = await fetch("https://ipapi.co/json/");
                const data = await res.json();
                setLocation({
                  lat: data.latitude,
                  lon: data.longitude,
                  label: data.city ? `${data.city}, ${data.country_name}` : "Detected Location",
                });
              } catch {
                setLocation(DEFAULT_LOC);
              } finally { setLoading(false); }
            }
          );
        } else {
          const res = await fetch("https://ipapi.co/json/");
          const data = await res.json();
          setLocation({
            lat: data.latitude,
            lon: data.longitude,
            label: data.city ? `${data.city}, ${data.country_name}` : "Detected Location",
          });
          setLoading(false);
        }
      } catch {
        setLocation(DEFAULT_LOC);
        setLoading(false);
      }
    }

    detect();
  }, []);

  function setPreference(newLoc) {
    // Ensure the location has valid coordinates
    if (newLoc && typeof newLoc.lat === "number" && typeof newLoc.lon === "number") {
      setLocation(newLoc);
      localStorage.setItem(LS_KEY, JSON.stringify(newLoc));
    }
  }

  function clearPreference() {
    localStorage.removeItem(LS_KEY);
    setLocation(DEFAULT_LOC);
  }

  return {
    location,
    setPreference,
    clearPreference,
    loading,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "Asia/Kolkata",
  };
}