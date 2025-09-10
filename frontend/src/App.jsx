import React, { useEffect, useMemo, useRef, useState } from "react";
// import { motion } from "framer-motion";
import { Sparkles, Star, Sun, Moon, Bot, Shield, CreditCard, Compass, Calendar, Users, Globe2, ChevronRight, MessageSquare, HeartHandshake, Cpu } from "lucide-react";
import Today from "./Today";

// If you use shadcn/ui in your stack, these imports will resolve.
// Otherwise, the fallback components below will be used.
let Button, Card, CardContent, CardHeader, CardTitle, Input, Textarea;
try {
  // eslint-disable-next-line @typescript-eslint/no-var-requires
  ({ Button } = require("@/components/ui/button"));
  ({ Card, CardContent, CardHeader, CardTitle } = require("@/components/ui/card"));
  ({ Input } = require("@/components/ui/input"));
  ({ Textarea } = require("@/components/ui/textarea"));
} catch (e) {
  // Fallback minimal components styled with Tailwind
  Button = ({ className = "", children, ...props }) => (
    <button className={`px-4 py-2 rounded-2xl shadow-sm hover:shadow md:font-medium ${className}`} {...props}>
      {children}
    </button>
  );
  Card = ({ className = "", children }) => (
    <div className={`rounded-2xl border border-white/10 bg-white/5 backdrop-blur p-4 ${className}`}>{children}</div>
  );
  CardHeader = ({ children, className = "" }) => <div className={`mb-2 ${className}`}>{children}</div>;
  CardTitle = ({ children, className = "" }) => <h3 className={`text-lg font-semibold ${className}`}>{children}</h3>;
  CardContent = ({ children, className = "" }) => <div className={className}>{children}</div>;
  Input = ({ className = "", ...props }) => (
    <input className={`w-full px-3 py-2 rounded-xl bg-white/90 text-gray-900 placeholder-gray-500 focus:outline-none shadow-sm ${className}`} {...props} />
  );
  Textarea = ({ className = "", ...props }) => (
    <textarea className={`w-full px-3 py-2 rounded-xl bg-white/90 text-gray-900 placeholder-gray-500 focus:outline-none shadow-sm ${className}`} {...props} />
  );
}

// Simple starry background
const Stars = () => {
  const canvasRef = useRef(null);
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    let raf;
    const dpr = window.devicePixelRatio || 1;

    const resize = () => {
      canvas.width = canvas.clientWidth * dpr;
      canvas.height = canvas.clientHeight * dpr;
    };
    resize();
    window.addEventListener("resize", resize);

    const stars = Array.from({ length: 140 }, () => ({
      x: Math.random(),
      y: Math.random(),
      r: Math.random() * 1.2 + 0.2,
      s: Math.random() * 0.5 + 0.2,
    }));

    const tick = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "rgba(255,255,255,0.9)";
      stars.forEach((st) => {
        const x = st.x * canvas.width;
        const y = st.y * canvas.height;
        const r = st.r * (0.5 + Math.sin(Date.now() * 0.002 * st.s) * 0.5);
        ctx.beginPath();
        ctx.arc(x, y, Math.max(0.2, r), 0, Math.PI * 2);
        ctx.fill();
      });
      raf = requestAnimationFrame(tick);
    };

    tick();
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("resize", resize);
    };
  }, []);

  return <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />;
};

const Feature = ({ icon: Icon, title, children }) => (
  <Card className="bg-white/5 border-white/10">
    <CardHeader>
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-xl bg-white/10"><Icon className="w-5 h-5" /></div>
        <CardTitle className="text-white">{title}</CardTitle>
      </div>
    </CardHeader>
    <CardContent className="text-sm text-white/80 leading-relaxed">{children}</CardContent>
  </Card>
);

const Check = ({ children }) => (
  <div className="flex items-start gap-3"><span className="mt-1 inline-flex h-5 w-5 items-center justify-center rounded-full bg-emerald-500/20"><svg viewBox="0 0 24 24" className="h-3.5 w-3.5"><path fill="currentColor" d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z"/></svg></span><span>{children}</span></div>
);

const Tier = ({ name, price, cta, features, highlighted }) => (
  <Card className={`relative ${highlighted ? "ring-2 ring-emerald-400" : ""}`}>
    {highlighted && (
      <div className="absolute -top-3 right-4 bg-emerald-500 text-white text-xs px-2 py-1 rounded-full">Popular</div>
    )}
    <CardHeader>
      <CardTitle className="text-white flex items-center gap-2">{name}</CardTitle>
    </CardHeader>
    <CardContent>
      <div className="text-4xl font-bold text-white">{price}<span className="text-base font-medium text-white/70">/mo</span></div>
      <ul className="mt-4 space-y-3 text-white/80 text-sm">
        {features.map((f, i) => (
          <li key={i} className="flex gap-2"><Star className="w-4 h-4 mt-0.5" /> {f}</li>
        ))}
      </ul>
      <Button className="mt-6 w-full bg-emerald-500 hover:bg-emerald-600 text-white">{cta}</Button>
    </CardContent>
  </Card>
);

const ChatBubble = ({ role, text }) => (
  <div className={`max-w-[85%] w-fit rounded-2xl px-4 py-2 text-sm leading-relaxed shadow-md ${role === "user" ? "bg-white text-gray-900 ml-auto" : "bg-white/10 text-white"}`}>
    {text}
  </div>
);

const ChatWidget = () => {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    { role: "assistant", text: "Hi! I’m your Astrooverz guide. Ask me about your numerology, today’s panchangam, or compatibility." },
  ]);

  const send = async () => {
    if (!input.trim()) return;
    const userMsg = { role: "user", text: input.trim() };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setLoading(true);
    try {
      // Backend placeholder: change to your FastAPI route
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: [...messages, userMsg].map(({ role, text }) => ({ role, content: text })),
        }),
      });
      if (!res.ok) throw new Error("Chat API error");
      const data = await res.json();
      const reply = data?.reply || "Here’s a sample response. Hook me to your LLM API at /api/chat.";
      setMessages((m) => [...m, { role: "assistant", text: reply }]);
    } catch (e) {
      setMessages((m) => [...m, { role: "assistant", text: "Hmm, I couldn’t reach the server. Check your /api/chat route." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {open ? (
        <Card className="w-[360px] sm:w-[420px] bg-gradient-to-b from-slate-900/95 to-slate-800/95 border-white/10 backdrop-blur-xl">
          <CardHeader className="flex flex-row items-center justify-between">
            <div className="flex items-center gap-2 text-white"><Bot className="w-5 h-5"/> Astrooverz Chat</div>
            <button onClick={() => setOpen(false)} className="text-white/80 hover:text-white">✕</button>
          </CardHeader>
          <CardContent>
            <div className="h-64 overflow-y-auto space-y-3 pr-1">
              {messages.map((m, idx) => <ChatBubble key={idx} role={m.role} text={m.text} />)}
              {loading && <ChatBubble role="assistant" text="Typing…" />}
            </div>
            <div className="mt-3 flex gap-2">
              <Input
                placeholder="Ask about numerology, panchangam, tarot…"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && send()}
              />
              <Button onClick={send} className="bg-emerald-500 hover:bg-emerald-600 text-white">Send</Button>
            </div>
          </CardContent>
        </Card>
      ) : (
        <Button onClick={() => setOpen(true)} className="bg-emerald-500 hover:bg-emerald-600 text-white shadow-lg flex items-center gap-2">
          <MessageSquare className="w-4 h-4"/> Ask Astrooverz
        </Button>
      )}
    </div>
  );
};

const KPI = ({ value, label }) => (
  <div className="text-center">
    <div className="text-3xl md:text-4xl font-bold text-white">{value}</div>
    <div className="text-xs md:text-sm text-white/70 mt-1">{label}</div>
  </div>
);

export default function AstrooverzLanding() {
  const [dob, setDob] = useState("");
  const [name, setName] = useState("");
  const [loc, setLoc] = useState("");
  const [timeOfBirth, setTimeOfBirth] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [currentPage, setCurrentPage] = useState("home");

  // Simple routing based on URL hash
  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.slice(1);
      setCurrentPage(hash || "home");
    };

    // Set initial page
    handleHashChange();

    // Listen for hash changes
    window.addEventListener("hashchange", handleHashChange);
    return () => window.removeEventListener("hashchange", handleHashChange);
  }, []);

  // Handle navigation
  const navigateTo = (page) => {
    setCurrentPage(page);
    window.location.hash = page;
  };

  const submitQuickReading = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      // Validate required fields
      if (!name || !dob || !timeOfBirth || !loc) {
        setResult({ error: "Please fill in all required fields: Name, Date of Birth, Time of Birth, and Location." });
        setLoading(false);
        return;
      }

      // Call the FastAPI quick reading endpoint
      const res = await fetch("/api/quick-reading", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          name, 
          dob, 
          time_of_birth: timeOfBirth,
          location: loc 
        })
      });
      
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to get reading");
      }
      
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: err.message || "Could not fetch reading. Please try again." });
    } finally {
      setLoading(false);
    }
  };

  const features = useMemo(() => ([
    { icon: Sun, title: "Vedic Panchangam", text: "Daily auspicious hours (Rahu, Yamaganda, Gulikai), sunrise/sunset, nakshatra & tithi tuned to your latitude/longitude as per ancient Maharishi wisdom." },
    { icon: Cpu, title: "Digital Jothidar", text: "Your personal astrologer powered by AI, blending traditional Vedic knowledge with modern technology for life guidance." },
    { icon: Shield, title: "Sacred Privacy", text: "Your birth details and readings are treated with the utmost respect and encrypted at rest and in transit." },
    { icon: Calendar, title: "Life's Timing", text: "Track planetary transits, dasha periods & auspicious moments. Get timely guidance for important life decisions." },
    { icon: Users, title: "Family Karma", text: "Add spouse, children, parents—create shared rituals, reminders, and compatibility insights for harmonious family life." },
    { icon: Globe2, title: "Ancient Wisdom, Modern Access", text: "Access the timeless wisdom of Vedic astrology anywhere, anytime through our modern digital platform." },
  ]), []);

  // Render different pages based on current route
  if (currentPage === "today") {
    return <Today />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-950 via-slate-950 to-slate-900 text-white relative overflow-hidden">
      <Stars />
      {/* NAV */}
      <nav className="relative z-10 max-w-7xl mx-auto px-4 md:px-8 py-5 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="p-1.5 rounded-xl bg-white/10">
            <Sparkles className="w-5 h-5" />
          </div>
          <span className="text-lg md:text-xl font-semibold tracking-wide">Astrooverz</span>
        </div>
        <div className="hidden md:flex items-center gap-6 text-white/80">
          <button onClick={() => navigateTo("today")} className="hover:text-white">Today's Panchangam</button>
          <button onClick={() => navigateTo("home")} className="hover:text-white">Home</button>
          <a href="#features" className="hover:text-white">Features</a>
          <a href="#how" className="hover:text-white">How it works</a>
          <a href="#pricing" className="hover:text-white">Pricing</a>
          <a href="#faq" className="hover:text-white">FAQ</a>
        </div>
        <div className="flex items-center gap-3">
          <Button className="bg-white/10 text-white hover:bg-white/20">Sign in</Button>
          <Button className="bg-emerald-500 hover:bg-emerald-600 text-white">Get started</Button>
        </div>
      </nav>

      {/* HERO */}
      <header className="relative z-10 max-w-7xl mx-auto px-4 md:px-8 py-12 md:py-20 grid md:grid-cols-2 gap-10 items-center">
        <div>
          <h1 className="text-4xl md:text-6xl font-extrabold leading-tight">
            Your Personal Time & Luck Mentor—
            <span className="bg-gradient-to-r from-emerald-300 to-emerald-500 bg-clip-text text-transparent"> powered by Vedic Wisdom</span>
          </h1>
          <p className="mt-5 text-white/80 md:text-lg max-w-xl">
            Astrooverz is your personalised digital jothidar, guiding life's important events and everyday choices with the wisdom of ancient Vedic astrology as envisioned by the Maharishis. Combining tradition with modern technology, Astrooverz helps you align with the right time, harness good fortune, and navigate life's journey with confidence.
          </p>
          <div className="mt-7 flex flex-wrap items-center gap-3">
            <Button className="bg-emerald-500 hover:bg-emerald-600 text-white flex items-center gap-2">Start free <ChevronRight className="w-4 h-4"/></Button>
            <Button className="bg-white/10 hover:bg-white/20 text-white flex items-center gap-2">Explore demo <Compass className="w-4 h-4"/></Button>
          </div>
          <div className="mt-10 grid grid-cols-3 gap-6">
            <KPI value="200k+" label="Guided sessions" />
            <KPI value="97%" label="User satisfaction" />
            <KPI value="25+" label="Cities timezones auto-adjust" />
          </div>
        </div>
        <div className="relative">
          <div className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl p-6 shadow-2xl">
            <div className="text-white/90 font-medium mb-3">Instant mini reading</div>
            <form onSubmit={submitQuickReading} className="space-y-3">
              <Input placeholder="Full Name" value={name} onChange={(e) => setName(e.target.value)} required />
              <Input type="date" placeholder="Date of Birth" value={dob} onChange={(e) => setDob(e.target.value)} required />
              <Input type="time" placeholder="Time of Birth" value={timeOfBirth} onChange={(e) => setTimeOfBirth(e.target.value)} required />
              <Input placeholder="Birth Location (City, Country)" value={loc} onChange={(e) => setLoc(e.target.value)} required />
              <Button type="submit" className="w-full bg-emerald-500 hover:bg-emerald-600 text-white" disabled={loading}>
                {loading ? "Calculating…" : "Get my quick reading"}
              </Button>
            </form>
            <div className="mt-4 min-h-20 text-sm text-white/90">
              {result && (
                <pre className="whitespace-pre-wrap text-xs bg-black/30 rounded-xl p-3 border border-white/10 max-h-48 overflow-auto">{JSON.stringify(result, null, 2)}</pre>
              )}
              {!result && (
                <p className="text-white/70 text-xs">We'll compute a comprehensive Vedic reading including numerology, panchangam insights, and life guidance. All fields are required for accurate analysis.</p>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* FEATURES */}
      <section id="features" className="relative z-10 max-w-7xl mx-auto px-4 md:px-8 py-14">
        <h2 className="text-2xl md:text-3xl font-bold">Designed for clarity and calm</h2>
        <p className="text-white/70 mt-2 max-w-2xl">All the wisdom you want—without the clutter. A lightweight, secure stack tuned for speed and privacy.</p>
        <div className="mt-8 grid md:grid-cols-3 gap-5">
          {features.map((f, i) => (
            <Feature key={i} icon={f.icon} title={f.title}>{f.text}</Feature>
          ))}
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section id="how" className="relative z-10 max-w-7xl mx-auto px-4 md:px-8 py-14">
        <div className="grid md:grid-cols-3 gap-6">
          <Card>
            <CardHeader><CardTitle className="text-white">1. Create your profile</CardTitle></CardHeader>
            <CardContent className="text-white/80 text-sm leading-relaxed">
              Add your name, birth details, and (optionally) family members for shared rituals and reminders.
            </CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle className="text-white">2. Connect the LLM</CardTitle></CardHeader>
            <CardContent className="text-white/80 text-sm leading-relaxed">
              Our API blends numerology and panchangam signals. You’ll get contextual guidance and Q&A through the chat widget.
            </CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle className="text-white">3. Act with confidence</CardTitle></CardHeader>
            <CardContent className="text-white/80 text-sm leading-relaxed">
              Daily windows, auspicious hours, and nudges—automatically adjusted to your location.
            </CardContent>
          </Card>
        </div>
      </section>

      {/* PRICING */}
      <section id="pricing" className="relative z-10 max-w-7xl mx-auto px-4 md:px-8 py-14">
        <h2 className="text-2xl md:text-3xl font-bold">Simple, transparent pricing</h2>
        <p className="text-white/70 mt-2 max-w-2xl">Start free. Upgrade when you want deeper insights and family features.</p>
        <div className="mt-8 grid md:grid-cols-3 gap-6">
          <Tier
            name="Free"
            price="₹0"
            cta="Start now"
            features={["Mini readings", "Daily panchangam", "LLM chat (lite)"]}
          />
          <Tier
            name="Pro"
            price="₹299"
            cta="Go Pro"
            highlighted
            features={["Full readings", "Family profiles (up to 4)", "Calendar sync & reminders", "LLM chat (standard)"]}
          />
          <Tier
            name="Premium"
            price="₹699"
            cta="Unlock Premium"
            features={["Advanced compatibility", "Priority support", "LLM chat (priority)", "Early features access"]}
          />
        </div>
      </section>

      {/* TESTIMONIALS / TRUST */}
      <section className="relative z-10 max-w-7xl mx-auto px-4 md:px-8 py-14">
        <div className="grid md:grid-cols-3 gap-6">
          <Card>
            <CardHeader><CardTitle className="text-white flex items-center gap-2"><HeartHandshake className="w-5 h-5"/> Trust</CardTitle></CardHeader>
            <CardContent className="text-white/80 text-sm">We never sell your data. Readings are generated on-demand and cached securely.</CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle className="text-white flex items-center gap-2"><CreditCard className="w-5 h-5"/> Payments</CardTitle></CardHeader>
            <CardContent className="text-white/80 text-sm">UPI, cards, and netbanking supported. Cancel anytime from your dashboard.</CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle className="text-white flex items-center gap-2"><Bot className="w-5 h-5"/> Roadmap</CardTitle></CardHeader>
            <CardContent className="text-white/80 text-sm">Tarot, vastu modules, and deeper LLM personalization are in active development.</CardContent>
          </Card>
        </div>
      </section>

      {/* FAQ */}
      <section id="faq" className="relative z-10 max-w-4xl mx-auto px-4 md:px-8 py-14">
        <h2 className="text-2xl md:text-3xl font-bold">Frequently asked</h2>
        <div className="mt-6 grid gap-4">
          <Card>
            <CardHeader><CardTitle className="text-white">Is this scientific or spiritual?</CardTitle></CardHeader>
            <CardContent className="text-white/80 text-sm">We present traditional frameworks (Vedic panchangam, numerology) transparently and let you decide how to use them alongside practical guidance.</CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle className="text-white">How does the LLM work here?</CardTitle></CardHeader>
            <CardContent className="text-white/80 text-sm">Your questions are routed to our API which augments an LLM with your profile’s numerology and the day’s panchangam context for relevant answers.</CardContent>
          </Card>
          <Card>
            <CardHeader><CardTitle className="text-white">Can I add my family?</CardTitle></CardHeader>
            <CardContent className="text-white/80 text-sm">Yes. Pro and Premium plans support multiple profiles with shared reminders.</CardContent>
          </Card>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="relative z-10 border-t border-white/10">
        <div className="max-w-7xl mx-auto px-4 md:px-8 py-8 grid md:grid-cols-4 gap-8 text-sm">
          <div>
            <div className="flex items-center gap-2 text-white font-semibold"><Sparkles className="w-4 h-4"/> Astrooverz</div>
            <p className="text-white/70 mt-2">Personalized guidance, built with privacy.</p>
          </div>
          <div>
            <div className="text-white/80 font-medium mb-2">Product</div>
            <ul className="space-y-1 text-white/60">
              <li><a href="#features" className="hover:text-white">Features</a></li>
              <li><a href="#pricing" className="hover:text-white">Pricing</a></li>
              <li><a href="#faq" className="hover:text-white">FAQ</a></li>
            </ul>
          </div>
          <div>
            <div className="text-white/80 font-medium mb-2">Legal</div>
            <ul className="space-y-1 text-white/60">
              <li>Terms</li>
              <li>Privacy</li>
              <li>Refund policy</li>
            </ul>
          </div>
          <div>
            <div className="text-white/80 font-medium mb-2">Stay in the loop</div>
            <div className="flex gap-2">
              <Input placeholder="your@email.com" />
              <Button className="bg-white text-gray-900 hover:bg-gray-100">Subscribe</Button>
            </div>
          </div>
        </div>
        <div className="text-center text-white/50 text-xs pb-6">© {new Date().getFullYear()} Astrooverz. All rights reserved.</div>
      </footer>

      {/* Floating LLM Chat */}
      <ChatWidget />
    </div>
  );
}
