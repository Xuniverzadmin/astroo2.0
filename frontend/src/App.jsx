import React from 'react';
import { AuthProvider } from './context/AuthContext';
import { ChatProvider } from './context/ChatContext';
import ChatPanel from './components/ChatPanel';
import { Toaster } from 'react-hot-toast';

function App() {
  return (
    <AuthProvider>
      <ChatProvider>
        <div className="App">
          <ChatPanel />
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