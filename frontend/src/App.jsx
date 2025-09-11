import React from 'react';
import { AuthProvider } from './context/AuthContext';
import { ChatProvider } from './context/ChatContext';
import ChatPanel from './components/ChatPanel';
import { Toaster } from 'react-hot-toast';

function App() {
  return (
    <AuthProvider>
      <ChatProvider>
        <div className="w-full min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 to-indigo-900">
          <div className="w-full max-w-lg md:max-w-2xl lg:max-w-4xl xl:max-w-6xl mx-auto px-2 py-6">
            <ChatPanel />
          </div>
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#1e293b',
                color: '#f1f5f9',
                border: '1px solid #334155'
              },
              success: {
                iconTheme: {
                  primary: '#10b981',
                  secondary: '#f1f5f9'
                }
              },
              error: {
                iconTheme: {
                  primary: '#ef4444',
                  secondary: '#f1f5f9'
                }
              }
            }}
          />
        </div>
      </ChatProvider>
    </AuthProvider>
  );
}

export default App;