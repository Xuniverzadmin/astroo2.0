// frontend/src/components/ChatPanel.jsx
import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Mic, MicOff, Settings, User, Moon, Sun } from 'lucide-react';
import { useChat } from '../context/ChatContext';
import { useAuth } from '../context/AuthContext';
import { useTranslation } from 'react-i18next';
import toast from 'react-hot-toast';

import QuickActions from './QuickActions';
import AuthModal from './AuthModal';
import ProfileMenu from './ProfileMenu';
import PanchangamWidgetStub from './PanchangamWidgetStub';
import ChartWidget from './ChartWidget';
import DashaWidget from './DashaWidget';
import RemindersWidget from './RemindersWidget';
import ProfileForm from './ProfileForm';

const ChatPanel = () => {
  const { t } = useTranslation();
  const { 
    messages, 
    isLoading, 
    activeWidgets, 
    sendMessage, 
    closeWidget,
    userPreferences,
    updatePreferences 
  } = useChat();
  const { isAuthenticated, currentProfile } = useAuth();
  
  const [inputValue, setInputValue] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [showAuth, setShowAuth] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(userPreferences.theme === 'dark');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSend = async (text = inputValue) => {
    if (!text.trim()) return;
    
    if (!isAuthenticated) {
      setShowAuth(true);
      return;
    }

    setInputValue('');
    await sendMessage(text);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const toggleRecording = () => {
    if (!isRecording) {
      // Start recording
      setIsRecording(true);
      toast.success('Recording started...');
      // TODO: Implement actual voice recording
      setTimeout(() => {
        setIsRecording(false);
        toast.success('Voice message recorded!');
        // Simulate voice-to-text
        handleSend("Show me today's panchangam");
      }, 3000);
    } else {
      // Stop recording
      setIsRecording(false);
      toast.success('Recording stopped');
    }
  };

  const toggleTheme = () => {
    const newTheme = isDarkMode ? 'light' : 'dark';
    setIsDarkMode(!isDarkMode);
    updatePreferences({ theme: newTheme });
    document.documentElement.classList.toggle('dark', !isDarkMode);
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
        return <ProfileForm onClose={() => closeWidget('profile')} />;
      default:
        return null;
    }
  };

  return (
    <div className="w-full h-screen flex flex-col items-center justify-center bg-gradient-to-br from-slate-950 to-indigo-900">
      {/* Header */}
      <div className="flex items-center justify-between p-4">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-3"
        >
          <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
            isDarkMode ? 'bg-indigo-600' : 'bg-indigo-500'
          }`}>
            <span className="text-white font-bold text-lg">A</span>
          </div>
          <div>
            <h1 className={`text-xl font-bold ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
              Astrooverz
            </h1>
            <p className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
              Your Vedic Astrology Guide
            </p>
          </div>
        </motion.div>

        <div className="flex items-center gap-2">
          <button
            onClick={toggleTheme}
            className={`p-2 rounded-lg transition-colors ${
              isDarkMode 
                ? 'hover:bg-slate-800 text-gray-400 hover:text-white' 
                : 'hover:bg-gray-200 text-gray-600 hover:text-gray-900'
            }`}
          >
            {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
          </button>
          
          <ProfileMenu onAuth={() => setShowAuth(true)} />
        </div>
      </div>

      {/* Main Chat Interface */}
      <div className="flex flex-col items-center justify-center px-4 pb-20">
        <motion.div
          layout
          className={`w-full max-w-lg md:max-w-2xl lg:max-w-4xl xl:max-w-6xl rounded-2xl shadow-2xl p-6 ${
            isDarkMode 
              ? 'bg-slate-900/80 backdrop-blur-sm border border-slate-800' 
              : 'bg-white/80 backdrop-blur-sm border border-gray-200'
          }`}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {/* Messages */}
          <div className="flex flex-col gap-4 h-96 overflow-y-auto mb-6 pr-2">
            <AnimatePresence>
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl ${
                      message.role === 'user'
                        ? isDarkMode
                          ? 'bg-indigo-600 text-white'
                          : 'bg-indigo-500 text-white'
                        : isDarkMode
                        ? 'bg-slate-800 text-gray-100'
                        : 'bg-gray-100 text-gray-900'
                    }`}
                  >
                    <p className="text-sm leading-relaxed">{message.content}</p>
                    {message.timestamp && (
                      <p className={`text-xs mt-1 ${
                        message.role === 'user' ? 'text-indigo-200' : 'text-gray-500'
                      }`}>
                        {new Date(message.timestamp).toLocaleTimeString()}
                      </p>
                    )}
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
            
            {isLoading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex justify-start"
              >
                <div className={`px-4 py-3 rounded-2xl ${
                  isDarkMode ? 'bg-slate-800' : 'bg-gray-100'
                }`}>
                  <div className="flex items-center gap-2">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                    <span className={`text-sm ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>
                      Thinking...
                    </span>
                  </div>
                </div>
              </motion.div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Actions */}
          <QuickActions onQuick={handleSend} />

          {/* Input Area */}
          <div className="flex items-center gap-3">
            <div className="flex-1 relative">
              <input
                ref={inputRef}
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={isAuthenticated ? "Ask me anything about Vedic astrology..." : "Sign in to start chatting..."}
                disabled={!isAuthenticated}
                className={`w-full px-4 py-3 rounded-xl border-0 focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-colors ${
                  isDarkMode
                    ? 'bg-slate-800 text-white placeholder-gray-400'
                    : 'bg-gray-100 text-gray-900 placeholder-gray-500'
                } ${!isAuthenticated ? 'opacity-50 cursor-not-allowed' : ''}`}
              />
            </div>
            
            <button
              onClick={toggleRecording}
              disabled={!isAuthenticated}
              className={`p-3 rounded-xl transition-colors ${
                isRecording
                  ? 'bg-red-500 text-white'
                  : isDarkMode
                  ? 'bg-slate-800 text-gray-400 hover:text-white hover:bg-slate-700'
                  : 'bg-gray-200 text-gray-600 hover:text-gray-900 hover:bg-gray-300'
              } ${!isAuthenticated ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
            </button>
            
            <button
              onClick={() => handleSend()}
              disabled={!inputValue.trim() || !isAuthenticated || isLoading}
              className={`p-3 rounded-xl transition-colors ${
                inputValue.trim() && isAuthenticated && !isLoading
                  ? 'bg-indigo-600 text-white hover:bg-indigo-700'
                  : isDarkMode
                  ? 'bg-slate-800 text-gray-400 cursor-not-allowed'
                  : 'bg-gray-200 text-gray-400 cursor-not-allowed'
              }`}
            >
              <Send size={20} />
            </button>
          </div>
        </motion.div>
      </div>

      {/* Active Widgets */}
      <AnimatePresence>
        {Object.entries(activeWidgets).map(([widgetType, widgetData]) => (
          <motion.div
            key={widgetType}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          >
            <motion.div
              initial={{ y: 20 }}
              animate={{ y: 0 }}
              exit={{ y: 20 }}
              className={`w-full max-w-lg md:max-w-2xl lg:max-w-4xl xl:max-w-6xl max-h-[90vh] overflow-y-auto rounded-2xl ${
                isDarkMode ? 'bg-slate-900' : 'bg-white'
              }`}
            >
              {getWidgetComponent(widgetType, widgetData.data)}
            </motion.div>
          </motion.div>
        ))}
      </AnimatePresence>

      {/* Auth Modal */}
      <AnimatePresence>
        {showAuth && (
          <AuthModal onClose={() => setShowAuth(false)} />
        )}
      </AnimatePresence>
    </div>
  );
};

export default ChatPanel;
