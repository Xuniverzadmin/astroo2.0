// frontend/src/components/ChatPanel.jsx
import React, { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Mic, MicOff, Settings, User, Moon, Sun, X, MapPin } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTranslation } from 'react-i18next';
import toast from 'react-hot-toast';
import { useLocation } from '../hooks/useLocation';

import QuickActions from './QuickActions';
import AuthModal from './AuthModal';
import ProfileMenu from './ProfileMenu';
import PanchangamWidgetStub from './PanchangamWidgetStub';
import ChartWidget from './ChartWidget';
import DashaWidget from './DashaWidget';
import RemindersWidget from './RemindersWidget';
import ProfileForm from './ProfileForm';
import LocationPicker from './LocationPicker';

const API_BASE = import.meta.env.VITE_API_URL || "https://api.astrooverz.com";

export default function ChatPanel() {
  const { t } = useTranslation();
  const { isAuthenticated, currentProfile } = useAuth();
  const { location, setPreference, clearPreference, loading: locLoading, timezone } = useLocation();
  
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Namaste! I can guide you using today's Panchangam. Ask me anything!" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [showAuth, setShowAuth] = useState(false);
  const [activeWidgets, setActiveWidgets] = useState({});
  const [isDarkMode, setIsDarkMode] = useState(true);
  const endRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => { 
    endRef.current?.scrollIntoView({ behavior: "smooth" }); 
  }, [messages, loading]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  async function sendMessage() {
    const text = input.trim();
    if (!text || loading) return;
    setError("");

    // optimistic user message
    setMessages(prev => [...prev, { role: "user", content: text }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/api/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: text,
          lat: location.lat,
          lon: location.lon,
          tz: timezone
        })
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();              // { answer: string }
      const reply = data.answer || "I couldn't generate a reply.";
      setMessages(prev => [...prev, { role: "assistant", content: reply }]);
    } catch (e) {
      setError(e?.message || "Something went wrong.");
      // optional: append an apologetic assistant bubble
      setMessages(prev => [...prev, { role: "assistant", content: "Sorry, I hit an error. Please try again." }]);
    } finally {
      setLoading(false);
    }
  }

  function onKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  const handleVoiceToggle = () => {
    if (isRecording) {
      setIsRecording(false);
      toast.success('Voice message recorded!');
      // Simulate voice-to-text
      setTimeout(() => {
        sendMessage("Show me today's panchangam");
      }, 3000);
    } else {
      setIsRecording(true);
      toast.success('Recording started...');
    }
  };

  const openWidget = (widgetType, data = {}) => {
    setActiveWidgets(prev => ({ ...prev, [widgetType]: data }));
  };

  const closeWidget = (widgetType) => {
    setActiveWidgets(prev => {
      const newWidgets = { ...prev };
      delete newWidgets[widgetType];
      return newWidgets;
    });
  };

  const getWidgetComponent = (widgetType, data) => {
    switch (widgetType) {
      case 'panchangam':
        return <PanchangamWidgetStub data={data} onClose={() => closeWidget('panchangam')} />;
      case 'birthchart':
        return <ChartWidget data={data} onClose={() => closeWidget('birthchart')} />;
      case 'dasha':
        return <DashaWidget data={data} onClose={() => closeWidget('dasha')} />;
      case 'reminders':
        return <RemindersWidget data={data} onClose={() => closeWidget('reminders')} />;
      case 'profile':
        return <ProfileForm data={data} onClose={() => closeWidget('profile')} />;
      default:
        return null;
    }
  };

  return (
    <div className="w-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-slate-700">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-indigo-600">
            <Moon size={24} className="text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Astrooverz</h1>
            <p className="text-gray-400">Your Vedic astrology companion</p>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsDarkMode(!isDarkMode)}
            className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
          >
            {isDarkMode ? <Sun size={20} className="text-gray-400" /> : <Moon size={20} className="text-gray-400" />}
          </button>
          
          {isAuthenticated ? (
            <ProfileMenu />
          ) : (
            <button
              onClick={() => setShowAuth(true)}
              className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              <User size={16} />
              Sign In
            </button>
          )}
        </div>
      </div>

      {/* Location bar */}
      <div className="p-3 border-b border-slate-800 bg-slate-900/60 sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <div className="text-sm">
            <MapPin size={16} className="inline mr-1" />
            <span className="opacity-80">Location:</span> {locLoading ? "Detecting…" : location.label}
            <span className="opacity-60"> • TZ: {timezone}</span>
          </div>
          <button 
            className="px-2 py-1 text-xs bg-slate-700 text-white rounded hover:bg-slate-600 transition-colors" 
            onClick={clearPreference} 
            title="Use auto-detected"
          >
            Reset to Auto
          </button>
        </div>
        <div className="mt-2">
          <LocationPicker
            value={location}
            onSelect={(loc) =>
              setPreference({ lat: loc.lat, lon: loc.lon, label: loc.label })
            }
          />
        </div>
      </div>

      {/* Quick Actions */}
      <div className="p-4 border-b border-slate-700">
        <QuickActions onAction={openWidget} />
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto space-y-3 p-4">
        {messages.map((m, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className={`max-w-xl rounded-2xl px-4 py-3 ${
              m.role === "assistant" 
                ? "bg-slate-800/60 text-slate-50 self-start" 
                : "bg-indigo-600 text-white self-end ml-auto"
            }`}
          >
            {m.content}
          </motion.div>
        ))}
        {loading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-xl rounded-2xl px-4 py-3 bg-slate-800/60 text-slate-50 self-start"
          >
            <div className="flex items-center gap-2">
              <div className="animate-pulse">typing…</div>
            </div>
          </motion.div>
        )}
        <div ref={endRef} />
      </div>

      {error && (
        <div className="px-4 pb-2 text-sm text-red-400">
          {error}
        </div>
      )}

      {/* Input Area */}
      <div className="p-4 border-t border-slate-700">
        <div className="flex gap-2">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              className="w-full bg-slate-800 text-white rounded-lg px-4 py-3 pr-12 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500"
              rows={2}
              placeholder="Ask me about Vedic astrology, panchangam, or your birth chart..."
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={onKeyDown}
            />
            <button
              onClick={handleVoiceToggle}
              className={`absolute right-2 top-2 p-2 rounded-lg transition-colors ${
                isRecording 
                  ? 'bg-red-600 hover:bg-red-700' 
                  : 'bg-slate-700 hover:bg-slate-600'
              }`}
            >
              {isRecording ? <MicOff size={16} className="text-white" /> : <Mic size={16} className="text-white" />}
            </button>
          </div>
          <button 
            className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            disabled={loading || !input.trim()} 
            onClick={sendMessage}
          >
            {loading ? "Sending…" : "Send"}
            <Send size={16} />
          </button>
        </div>
      </div>

      {/* Widgets */}
      <AnimatePresence>
        {Object.entries(activeWidgets).map(([widgetType, data]) => (
          <React.Fragment key={widgetType}>
            {getWidgetComponent(widgetType, data)}
          </React.Fragment>
        ))}
      </AnimatePresence>

      {/* Auth Modal */}
      {showAuth && (
        <AuthModal onClose={() => setShowAuth(false)} />
      )}
    </div>
  );
}