import React, { useState, useEffect, useMemo } from 'react';
import { 
  Sun, 
  Moon, 
  Clock, 
  MapPin, 
  Calendar, 
  Download,
  RefreshCw,
  AlertTriangle,
  CheckCircle,
  XCircle
} from 'lucide-react';
import { useLocation } from '../hooks/useLocation';

// Utility functions
const formatTime = (timeString) => {
  if (!timeString) return '--:--';
  const date = new Date(timeString);
  return date.toLocaleTimeString('en-IN', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: true 
  });
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-IN', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

const getTimeRemaining = (endTime) => {
  if (!endTime) return null;
  const now = new Date();
  const end = new Date(endTime);
  const diff = end - now;
  
  if (diff <= 0) return null;
  
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  
  return { hours, minutes };
};

const getAuspiciousStatus = (period) => {
  if (!period) return { status: 'unknown', color: 'gray' };
  
  const now = new Date();
  const start = new Date(period.start);
  const end = new Date(period.end);
  
  if (now >= start && now <= end) {
    return { status: 'active', color: 'red' };
  } else if (now < start) {
    return { status: 'upcoming', color: 'yellow' };
  } else {
    return { status: 'passed', color: 'green' };
  }
};

const TodayCard = () => {
  const { location, loading: locationLoading, error: locationError, hasLocation } = useLocation();
  const [panchangam, setPanchangam] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  // Get today's date in YYYY-MM-DD format
  const today = useMemo(() => {
    return new Date().toISOString().split('T')[0];
  }, []);

  // Fetch panchangam data
  const fetchPanchangam = async () => {
    if (!hasLocation) {
      setError('Location is required to fetch panchangam data');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({
        lat: location.latitude.toString(),
        lon: location.longitude.toString(),
        tz: location.timezone
      });

      const response = await fetch(`/api/panchangam/${today}?${params}`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch panchangam: ${response.status}`);
      }

      const data = await response.json();
      setPanchangam(data);
      setLastUpdated(new Date());
    } catch (err) {
      setError(err.message || 'Failed to fetch panchangam data');
    } finally {
      setLoading(false);
    }
  };

  // Fetch data on mount and when location changes
  useEffect(() => {
    if (hasLocation) {
      fetchPanchangam();
    }
  }, [hasLocation, location.latitude, location.longitude, location.timezone, today]);

  // Update countdown timers every minute
  useEffect(() => {
    if (!panchangam) return;

    const interval = setInterval(() => {
      // Force re-render to update countdowns
      setLastUpdated(new Date());
    }, 60000); // Update every minute

    return () => clearInterval(interval);
  }, [panchangam]);

  // Generate ICS file for calendar download
  const generateICS = () => {
    if (!panchangam) return;

    const events = [];
    const date = new Date(panchangam.date);
    
    // Add sunrise/sunset
    events.push({
      title: 'Sunrise',
      start: new Date(panchangam.sunrise),
      end: new Date(panchangam.sunrise)
    });
    
    events.push({
      title: 'Sunset',
      start: new Date(panchangam.sunset),
      end: new Date(panchangam.sunset)
    });

    // Add inauspicious periods
    const inauspiciousPeriods = [
      { name: 'Rahu Kalam', period: panchangam.rahu_kalam },
      { name: 'Yama Gandam', period: panchangam.yama_gandam },
      { name: 'Gulikai Kalam', period: panchangam.gulikai_kalam }
    ];

    inauspiciousPeriods.forEach(({ name, period }) => {
      if (period) {
        events.push({
          title: `${name} (Avoid)`,
          start: new Date(period.start),
          end: new Date(period.end)
        });
      }
    });

    // Add Gowri periods
    if (panchangam.gowri_panchangam?.periods) {
      const gowriPeriods = panchangam.gowri_panchangam.periods;
      Object.entries(gowriPeriods).forEach(([name, period]) => {
        if (period) {
          const isAuspicious = panchangam.gowri_panchangam.auspicious.includes(name);
          events.push({
            title: `${name} (${isAuspicious ? 'Good' : 'Avoid'})`,
            start: new Date(period.start),
            end: new Date(period.end)
          });
        }
      });
    }

    // Generate ICS content
    let icsContent = [
      'BEGIN:VCALENDAR',
      'VERSION:2.0',
      'PRODID:-//Astrooverz//Panchangam//EN',
      'CALSCALE:GREGORIAN',
      'METHOD:PUBLISH'
    ];

    events.forEach(event => {
      const formatICSDate = (date) => {
        return date.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
      };

      icsContent.push(
        'BEGIN:VEVENT',
        `UID:${Date.now()}-${Math.random().toString(36).substr(2, 9)}@astrooverz.com`,
        `DTSTART:${formatICSDate(event.start)}`,
        `DTEND:${formatICSDate(event.end)}`,
        `SUMMARY:${event.title}`,
        `DESCRIPTION:Panchangam event for ${formatDate(panchangam.date)}`,
        'STATUS:CONFIRMED',
        'TRANSP:OPAQUE',
        'END:VEVENT'
      );
    });

    icsContent.push('END:VCALENDAR');

    // Download file
    const blob = new Blob([icsContent.join('\r\n')], { type: 'text/calendar' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `panchangam-${today}.ics`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  if (locationLoading) {
    return (
      <div className="bg-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-xl">
        <div className="flex items-center justify-center py-8">
          <RefreshCw className="w-6 h-6 animate-spin text-emerald-400" />
          <span className="ml-2 text-white/80">Getting your location...</span>
        </div>
      </div>
    );
  }

  if (locationError) {
    return (
      <div className="bg-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-xl">
        <div className="flex items-center gap-3 text-red-400 mb-4">
          <AlertTriangle className="w-5 h-5" />
          <span className="font-medium">Location Error</span>
        </div>
        <p className="text-white/80 text-sm mb-4">{locationError}</p>
        <button 
          onClick={() => window.location.reload()}
          className="bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-xl text-sm"
        >
          Try Again
        </button>
      </div>
    );
  }

  if (!hasLocation) {
    return (
      <div className="bg-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-xl">
        <div className="flex items-center gap-3 text-yellow-400 mb-4">
          <MapPin className="w-5 h-5" />
          <span className="font-medium">Location Required</span>
        </div>
        <p className="text-white/80 text-sm mb-4">
          Please allow location access to view today's panchangam.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Sun className="w-5 h-5 text-yellow-400" />
            Today's Panchangam
          </h2>
          <p className="text-white/70 text-sm">
            {formatDate(panchangam?.date || today)}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={fetchPanchangam}
            disabled={loading}
            className="p-2 rounded-xl bg-white/10 hover:bg-white/20 text-white/80 hover:text-white transition-colors"
            title="Refresh"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
          {panchangam && (
            <button
              onClick={generateICS}
              className="p-2 rounded-xl bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-400 hover:text-emerald-300 transition-colors"
              title="Add to Calendar"
            >
              <Download className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Location Info */}
      <div className="flex items-center gap-2 text-white/70 text-sm mb-6">
        <MapPin className="w-4 h-4" />
        <span>
          {location.city && location.country 
            ? `${location.city}, ${location.country}` 
            : `${location.latitude?.toFixed(4)}, ${location.longitude?.toFixed(4)}`
          }
        </span>
        <span className="text-white/50">•</span>
        <span>{location.timezone}</span>
      </div>

      {loading && !panchangam && (
        <div className="flex items-center justify-center py-8">
          <RefreshCw className="w-6 h-6 animate-spin text-emerald-400" />
          <span className="ml-2 text-white/80">Loading panchangam...</span>
        </div>
      )}

      {error && (
        <div className="flex items-center gap-3 text-red-400 mb-4">
          <XCircle className="w-5 h-5" />
          <span className="text-sm">{error}</span>
        </div>
      )}

      {panchangam && (
        <>
          {/* Sunrise/Sunset */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="bg-white/5 rounded-xl p-4">
              <div className="flex items-center gap-2 text-yellow-400 mb-2">
                <Sun className="w-4 h-4" />
                <span className="text-sm font-medium">Sunrise</span>
              </div>
              <div className="text-lg font-bold text-white">
                {formatTime(panchangam.sunrise)}
              </div>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <div className="flex items-center gap-2 text-orange-400 mb-2">
                <Moon className="w-4 h-4" />
                <span className="text-sm font-medium">Sunset</span>
              </div>
              <div className="text-lg font-bold text-white">
                {formatTime(panchangam.sunset)}
              </div>
            </div>
          </div>

          {/* Panchangam Elements */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="bg-white/5 rounded-xl p-4">
              <div className="text-sm text-white/70 mb-1">Tithi</div>
              <div className="text-lg font-bold text-white mb-1">
                {panchangam.tithi?.name}
              </div>
              <div className="text-xs text-white/60">
                {panchangam.tithi?.percentage?.toFixed(1)}% complete
              </div>
            </div>
            <div className="bg-white/5 rounded-xl p-4">
              <div className="text-sm text-white/70 mb-1">Nakshatra</div>
              <div className="text-lg font-bold text-white mb-1">
                {panchangam.nakshatra?.name}
              </div>
              <div className="text-xs text-white/60">
                {panchangam.nakshatra?.percentage?.toFixed(1)}% complete
              </div>
            </div>
          </div>

          {/* Inauspicious Periods */}
          <div className="mb-6">
            <h3 className="text-sm font-medium text-white/80 mb-3 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-red-400" />
              Avoid These Times
            </h3>
            <div className="space-y-3">
              {[
                { name: 'Rahu Kalam', period: panchangam.rahu_kalam, icon: '🔴' },
                { name: 'Yama Gandam', period: panchangam.yama_gandam, icon: '🟡' },
                { name: 'Gulikai Kalam', period: panchangam.gulikai_kalam, icon: '🟠' }
              ].map(({ name, period, icon }) => {
                const status = getAuspiciousStatus(period);
                const timeRemaining = getTimeRemaining(period?.end);
                
                return (
                  <div key={name} className="bg-white/5 rounded-xl p-3">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-lg">{icon}</span>
                        <span className="text-sm font-medium text-white">{name}</span>
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          status.status === 'active' ? 'bg-red-500/20 text-red-400' :
                          status.status === 'upcoming' ? 'bg-yellow-500/20 text-yellow-400' :
                          'bg-green-500/20 text-green-400'
                        }`}>
                          {status.status}
                        </span>
                      </div>
                      {timeRemaining && (
                        <div className="text-xs text-white/60">
                          {timeRemaining.hours}h {timeRemaining.minutes}m left
                        </div>
                      )}
                    </div>
                    <div className="text-sm text-white/80">
                      {formatTime(period?.start)} - {formatTime(period?.end)}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Gowri Panchangam */}
          {panchangam.gowri_panchangam && (
            <div className="mb-6">
              <h3 className="text-sm font-medium text-white/80 mb-3 flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-400" />
                Gowri Panchangam
              </h3>
              <div className="grid grid-cols-2 gap-2">
                {Object.entries(panchangam.gowri_panchangam.periods || {}).map(([name, period]) => {
                  const isAuspicious = panchangam.gowri_panchangam.auspicious.includes(name);
                  const status = getAuspiciousStatus(period);
                  
                  return (
                    <div key={name} className={`rounded-lg p-2 text-xs ${
                      isAuspicious 
                        ? 'bg-green-500/10 border border-green-500/20' 
                        : 'bg-red-500/10 border border-red-500/20'
                    }`}>
                      <div className="flex items-center justify-between mb-1">
                        <span className={`font-medium ${
                          isAuspicious ? 'text-green-400' : 'text-red-400'
                        }`}>
                          {name}
                        </span>
                        <span className={`px-1 py-0.5 rounded text-xs ${
                          status.status === 'active' ? 'bg-yellow-500/20 text-yellow-400' :
                          status.status === 'upcoming' ? 'bg-blue-500/20 text-blue-400' :
                          'bg-gray-500/20 text-gray-400'
                        }`}>
                          {status.status}
                        </span>
                      </div>
                      <div className="text-white/70">
                        {formatTime(period?.start)} - {formatTime(period?.end)}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Last Updated */}
          {lastUpdated && (
            <div className="text-xs text-white/50 text-center pt-4 border-t border-white/10">
              Last updated: {lastUpdated.toLocaleTimeString('en-IN')}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default TodayCard;
