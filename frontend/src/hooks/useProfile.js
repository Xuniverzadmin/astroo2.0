// frontend/src/hooks/useProfile.js
import { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { useLocalStorage } from './useLocalStorage';

export const useProfile = () => {
  const { currentProfile, profiles, addProfile, updateProfile, deleteProfile, switchProfile } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [locationData, setLocationData] = useLocalStorage('astrooverz_location', null);

  // Get user's current location
  const getCurrentLocation = useCallback(() => {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Geolocation is not supported by this browser'));
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          const location = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy,
            timestamp: new Date().toISOString()
          };
          setLocationData(location);
          resolve(location);
        },
        (error) => {
          console.error('Geolocation error:', error);
          reject(error);
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 300000 // 5 minutes
        }
      );
    });
  }, [setLocationData]);

  // Create a new profile
  const createProfile = useCallback(async (profileData) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // If no location provided, try to get current location
      let location = profileData.location;
      if (!location && !profileData.latitude && !profileData.longitude) {
        try {
          const currentLocation = await getCurrentLocation();
          location = {
            latitude: currentLocation.latitude,
            longitude: currentLocation.longitude,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
          };
        } catch (geoError) {
          console.warn('Could not get current location:', geoError);
          // Use default location (Chennai, India)
          location = {
            latitude: 13.0827,
            longitude: 80.2707,
            timezone: 'Asia/Kolkata'
          };
        }
      }

      const newProfile = addProfile({
        ...profileData,
        ...location
      });

      return { success: true, profile: newProfile };
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setIsLoading(false);
    }
  }, [addProfile, getCurrentLocation]);

  // Update an existing profile
  const modifyProfile = useCallback(async (profileId, updates) => {
    setIsLoading(true);
    setError(null);
    
    try {
      updateProfile(profileId, updates);
      return { success: true };
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setIsLoading(false);
    }
  }, [updateProfile]);

  // Delete a profile
  const removeProfile = useCallback(async (profileId) => {
    setIsLoading(true);
    setError(null);
    
    try {
      deleteProfile(profileId);
      return { success: true };
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setIsLoading(false);
    }
  }, [deleteProfile]);

  // Switch to a different profile
  const changeProfile = useCallback((profileId) => {
    switchProfile(profileId);
  }, [switchProfile]);

  // Get profile by ID
  const getProfileById = useCallback((profileId) => {
    return profiles.find(profile => profile.id === profileId);
  }, [profiles]);

  // Calculate age from birth date
  const calculateAge = useCallback((birthDate) => {
    if (!birthDate) return null;
    
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    
    return age;
  }, []);

  // Get current profile age
  const currentProfileAge = currentProfile ? calculateAge(currentProfile.birthDate) : null;

  // Validate profile data
  const validateProfile = useCallback((profileData) => {
    const errors = {};
    
    if (!profileData.name?.trim()) {
      errors.name = 'Name is required';
    }
    
    if (!profileData.birthDate) {
      errors.birthDate = 'Birth date is required';
    } else {
      const birthDate = new Date(profileData.birthDate);
      const today = new Date();
      if (birthDate > today) {
        errors.birthDate = 'Birth date cannot be in the future';
      }
    }
    
    if (!profileData.birthTime) {
      errors.birthTime = 'Birth time is required';
    }
    
    if (!profileData.location?.trim()) {
      errors.location = 'Birth place is required';
    }
    
    if (!profileData.latitude || isNaN(parseFloat(profileData.latitude))) {
      errors.latitude = 'Valid latitude is required';
    }
    
    if (!profileData.longitude || isNaN(parseFloat(profileData.longitude))) {
      errors.longitude = 'Valid longitude is required';
    }
    
    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  }, []);

  return {
    // State
    currentProfile,
    profiles,
    isLoading,
    error,
    locationData,
    currentProfileAge,
    
    // Actions
    createProfile,
    modifyProfile,
    removeProfile,
    changeProfile,
    getProfileById,
    getCurrentLocation,
    calculateAge,
    validateProfile,
    
    // Utilities
    clearError: () => setError(null)
  };
};
