import { useState, useEffect, useCallback } from 'react';

/**
 * Custom hook for handling geolocation and manual location override
 * Provides current location, loading state, and error handling
 */
export const useLocation = () => {
  const [location, setLocation] = useState({
    latitude: null,
    longitude: null,
    timezone: 'Asia/Kolkata',
    city: '',
    country: ''
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [permissionDenied, setPermissionDenied] = useState(false);

  // Get current position using browser geolocation
  const getCurrentPosition = useCallback(() => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by this browser');
      return;
    }

    setLoading(true);
    setError(null);

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
          const { latitude, longitude } = position.coords;
          
          // Get timezone and location details using reverse geocoding
          const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
          
          // Try to get city name from reverse geocoding
          let city = '';
          let country = '';
          
          try {
            const response = await fetch(
              `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`
            );
            if (response.ok) {
              const data = await response.json();
              city = data.city || data.locality || '';
              country = data.countryName || '';
            }
          } catch (geocodeError) {
            console.warn('Reverse geocoding failed:', geocodeError);
          }

          setLocation({
            latitude,
            longitude,
            timezone,
            city,
            country
          });
          
          // Store in localStorage for future use
          localStorage.setItem('astrooverz_location', JSON.stringify({
            latitude,
            longitude,
            timezone,
            city,
            country
          }));
          
        } catch (err) {
          setError('Failed to get location details');
        } finally {
          setLoading(false);
        }
      },
      (error) => {
        setLoading(false);
        switch (error.code) {
          case error.PERMISSION_DENIED:
            setError('Location access denied by user');
            setPermissionDenied(true);
            break;
          case error.POSITION_UNAVAILABLE:
            setError('Location information is unavailable');
            break;
          case error.TIMEOUT:
            setError('Location request timed out');
            break;
          default:
            setError('An unknown error occurred while retrieving location');
            break;
        }
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 300000 // 5 minutes
      }
    );
  }, []);

  // Set location manually
  const setManualLocation = useCallback((lat, lon, tz = 'Asia/Kolkata', city = '', country = '') => {
    const newLocation = {
      latitude: parseFloat(lat),
      longitude: parseFloat(lon),
      timezone: tz,
      city,
      country
    };
    
    setLocation(newLocation);
    setError(null);
    
    // Store in localStorage
    localStorage.setItem('astrooverz_location', JSON.stringify(newLocation));
  }, []);

  // Clear location
  const clearLocation = useCallback(() => {
    setLocation({
      latitude: null,
      longitude: null,
      timezone: 'Asia/Kolkata',
      city: '',
      country: ''
    });
    setError(null);
    setPermissionDenied(false);
    localStorage.removeItem('astrooverz_location');
  }, []);

  // Load saved location on mount
  useEffect(() => {
    const savedLocation = localStorage.getItem('astrooverz_location');
    if (savedLocation) {
      try {
        const parsed = JSON.parse(savedLocation);
        setLocation(parsed);
      } catch (err) {
        console.warn('Failed to parse saved location:', err);
        localStorage.removeItem('astrooverz_location');
      }
    }
  }, []);

  // Auto-request location if not available and permission not denied
  useEffect(() => {
    if (!location.latitude && !permissionDenied && !loading) {
      getCurrentPosition();
    }
  }, [location.latitude, permissionDenied, loading, getCurrentPosition]);

  return {
    location,
    loading,
    error,
    permissionDenied,
    getCurrentPosition,
    setManualLocation,
    clearLocation,
    hasLocation: location.latitude !== null && location.longitude !== null
  };
};
