// frontend/src/context/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { useLocalStorage } from '../hooks/useLocalStorage';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [currentProfile, setCurrentProfile] = useState(null);
  const [profiles, setProfiles] = useState([]);
  
  // Local storage hooks
  const [storedUser, setStoredUser] = useLocalStorage('astrooverz_user', null);
  const [storedProfiles, setStoredProfiles] = useLocalStorage('astrooverz_profiles', []);
  const [storedCurrentProfile, setStoredCurrentProfile] = useLocalStorage('astrooverz_current_profile', null);

  useEffect(() => {
    // Initialize from localStorage
    if (storedUser) {
      setUser(storedUser);
      setIsAuthenticated(true);
    }
    if (storedProfiles.length > 0) {
      setProfiles(storedProfiles);
    }
    if (storedCurrentProfile) {
      setCurrentProfile(storedCurrentProfile);
    }
    setIsLoading(false);
  }, []);

  const signIn = async (userData) => {
    try {
      const user = {
        id: Date.now().toString(),
        name: userData.name,
        email: userData.email || null,
        avatar: userData.avatar || null,
        createdAt: new Date().toISOString(),
        isGuest: !userData.email
      };
      
      setUser(user);
      setIsAuthenticated(true);
      setStoredUser(user);
      
      // If this is a new user, create a default profile
      if (userData.birthDate && userData.birthTime && userData.location) {
        const defaultProfile = {
          id: Date.now().toString(),
          name: userData.name,
          birthDate: userData.birthDate,
          birthTime: userData.birthTime,
          location: userData.location,
          latitude: userData.latitude || 0,
          longitude: userData.longitude || 0,
          timezone: userData.timezone || 'Asia/Kolkata',
          isDefault: true
        };
        
        addProfile(defaultProfile);
        setCurrentProfile(defaultProfile);
        setStoredCurrentProfile(defaultProfile);
      }
      
      return { success: true, user };
    } catch (error) {
      console.error('Sign in error:', error);
      return { success: false, error: error.message };
    }
  };

  const signOut = () => {
    setUser(null);
    setIsAuthenticated(false);
    setCurrentProfile(null);
    setProfiles([]);
    setStoredUser(null);
    setStoredProfiles([]);
    setStoredCurrentProfile(null);
  };

  const addProfile = (profileData) => {
    const newProfile = {
      id: Date.now().toString(),
      ...profileData,
      createdAt: new Date().toISOString()
    };
    
    const updatedProfiles = [...profiles, newProfile];
    setProfiles(updatedProfiles);
    setStoredProfiles(updatedProfiles);
    
    // If this is the first profile, set it as current
    if (profiles.length === 0) {
      setCurrentProfile(newProfile);
      setStoredCurrentProfile(newProfile);
    }
    
    return newProfile;
  };

  const updateProfile = (profileId, updates) => {
    const updatedProfiles = profiles.map(profile => 
      profile.id === profileId ? { ...profile, ...updates } : profile
    );
    setProfiles(updatedProfiles);
    setStoredProfiles(updatedProfiles);
    
    // Update current profile if it's the one being updated
    if (currentProfile?.id === profileId) {
      const updatedCurrentProfile = { ...currentProfile, ...updates };
      setCurrentProfile(updatedCurrentProfile);
      setStoredCurrentProfile(updatedCurrentProfile);
    }
  };

  const deleteProfile = (profileId) => {
    const updatedProfiles = profiles.filter(profile => profile.id !== profileId);
    setProfiles(updatedProfiles);
    setStoredProfiles(updatedProfiles);
    
    // If we deleted the current profile, switch to another one
    if (currentProfile?.id === profileId) {
      const newCurrentProfile = updatedProfiles[0] || null;
      setCurrentProfile(newCurrentProfile);
      setStoredCurrentProfile(newCurrentProfile);
    }
  };

  const switchProfile = (profileId) => {
    const profile = profiles.find(p => p.id === profileId);
    if (profile) {
      setCurrentProfile(profile);
      setStoredCurrentProfile(profile);
    }
  };

  const continueAsGuest = () => {
    const guestUser = {
      id: 'guest_' + Date.now().toString(),
      name: 'Guest User',
      email: null,
      avatar: null,
      createdAt: new Date().toISOString(),
      isGuest: true
    };
    
    setUser(guestUser);
    setIsAuthenticated(true);
    setStoredUser(guestUser);
    
    return { success: true, user: guestUser };
  };

  const value = {
    user,
    isAuthenticated,
    isLoading,
    currentProfile,
    profiles,
    signIn,
    signOut,
    addProfile,
    updateProfile,
    deleteProfile,
    switchProfile,
    continueAsGuest
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
