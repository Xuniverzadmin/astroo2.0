// frontend/src/context/ChatContext.jsx
import React, { createContext, useContext, useState, useCallback } from 'react';
import { useLocalStorage } from '../hooks/useLocalStorage';
import toast from 'react-hot-toast';

const ChatContext = createContext();

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeWidgets, setActiveWidgets] = useState({});
  const [chatHistory, setChatHistory] = useLocalStorage('astrooverz_chat_history', []);
  const [userPreferences, setUserPreferences] = useLocalStorage('astrooverz_preferences', {
    language: 'en',
    timezone: 'Asia/Kolkata',
    theme: 'dark'
  });

  // Initialize with welcome message
  React.useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        {
          id: 'welcome',
          role: 'assistant',
          content: 'Namaste! I\'m your Vedic astrology guide. How can I help you today?',
          timestamp: new Date().toISOString(),
          type: 'text'
        }
      ]);
    }
  }, []);

  const sendMessage = useCallback(async (content, type = 'text') => {
    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
      type
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Simulate API call to backend chat endpoint
      const response = await simulateChatAPI(content, userPreferences);
      
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.content,
        timestamp: new Date().toISOString(),
        type: response.type || 'text',
        widget: response.widget || null,
        data: response.data || null
      };

      setMessages(prev => [...prev, assistantMessage]);
      
      // Save to chat history
      setChatHistory(prev => [...prev, userMessage, assistantMessage]);
      
      // Handle widget activation
      if (response.widget) {
        setActiveWidgets(prev => ({
          ...prev,
          [response.widget]: {
            type: response.widget,
            data: response.data,
            timestamp: new Date().toISOString()
          }
        }));
      }

    } catch (error) {
      console.error('Chat error:', error);
      toast.error('Sorry, I encountered an error. Please try again.');
      
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'I apologize, but I encountered an error. Please try again or rephrase your question.',
        timestamp: new Date().toISOString(),
        type: 'error'
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [userPreferences]);

  const clearChat = () => {
    setMessages([
      {
        id: 'welcome',
        role: 'assistant',
        content: 'Namaste! I\'m your Vedic astrology guide. How can I help you today?',
        timestamp: new Date().toISOString(),
        type: 'text'
      }
    ]);
    setChatHistory([]);
    setActiveWidgets({});
  };

  const closeWidget = (widgetType) => {
    setActiveWidgets(prev => {
      const updated = { ...prev };
      delete updated[widgetType];
      return updated;
    });
  };

  const updatePreferences = (newPreferences) => {
    setUserPreferences(prev => ({ ...prev, ...newPreferences }));
  };

  const value = {
    messages,
    isLoading,
    activeWidgets,
    chatHistory,
    userPreferences,
    sendMessage,
    clearChat,
    closeWidget,
    updatePreferences
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};

// Simulate chat API - replace with actual backend call
const simulateChatAPI = async (content, preferences) => {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));

  const lowerContent = content.toLowerCase();
  
  // Handle different types of requests
  if (lowerContent.includes('panchangam') || lowerContent.includes('today')) {
    return {
      content: "Here's today's Panchangam for you! 🌅",
      type: 'widget',
      widget: 'panchangam',
      data: {
        date: new Date().toISOString().split('T')[0],
        location: { latitude: 12.9716, longitude: 77.5946, timezone: preferences.timezone }
      }
    };
  }
  
  if (lowerContent.includes('chart') || lowerContent.includes('birth chart') || lowerContent.includes('kundali')) {
    return {
      content: "Let me show you your birth chart! 🔮",
      type: 'widget',
      widget: 'birthchart',
      data: { profileId: 'current' }
    };
  }
  
  if (lowerContent.includes('dasha') || lowerContent.includes('planetary period')) {
    return {
      content: "Here's your Dasha timeline! ⏰",
      type: 'widget',
      widget: 'dasha',
      data: { profileId: 'current' }
    };
  }
  
  if (lowerContent.includes('reminder') || lowerContent.includes('event')) {
    return {
      content: "Let me show you your reminders and events! 📅",
      type: 'widget',
      widget: 'reminders',
      data: {}
    };
  }
  
  if (lowerContent.includes('profile') || lowerContent.includes('add profile')) {
    return {
      content: "I'll help you add a new profile! 👤",
      type: 'widget',
      widget: 'profile',
      data: {}
    };
  }
  
  // Default response
  const responses = [
    "I understand you're interested in Vedic astrology. Could you be more specific about what you'd like to know?",
    "That's a great question! I can help you with Panchangam, birth charts, Dasha periods, or general astrology guidance.",
    "I'm here to help with all your Vedic astrology needs. What would you like to explore today?",
    "Namaste! I can assist you with daily Panchangam, birth chart analysis, planetary periods, and more."
  ];
  
  return {
    content: responses[Math.floor(Math.random() * responses.length)],
    type: 'text'
  };
};
