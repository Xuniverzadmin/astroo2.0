// Real ChartWidget that calls the backend API
import { motion } from 'framer-motion';
import { Loader2, User, X } from 'lucide-react';
import React, { useEffect, useState } from 'react';
import { apiJSON } from '../api';

export default function ChartWidget({ data, onClose }) {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (data?.profile) {
      fetchBirthChart();
    }
  }, [data?.profile]);

  const fetchBirthChart = async () => {
    try {
      setLoading(true);
      setError(null);

      const profile = data.profile;
      console.log('Fetching birth chart for profile:', profile);

      // Prepare birth data for API
      const birthData = {
        name: profile.name || 'User',
        birth_date: profile.birth_date || '1990-01-01',
        birth_time: profile.birth_time || '12:00',
        birth_place: profile.birth_place || 'Chennai',
        latitude: profile.latitude || 13.0827,
        longitude: profile.longitude || 80.2707,
        timezone: profile.timezone || 'Asia/Kolkata'
      };

      console.log('Sending birth data to API:', birthData);
      const result = await apiJSON('/api/birth-chart/calculate', {
        method: 'POST',
        body: JSON.stringify(birthData)
      });

      console.log('Birth chart API response:', result);
      setChartData(result);
    } catch (err) {
      console.error('Error fetching birth chart:', err);
      setError(err.message || 'Failed to load birth chart data');
    } finally {
      setLoading(false);
    }
  };
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
    >
      <div className="bg-slate-900 rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-700">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-violet-600">
              <User size={24} className="text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">Birth Chart</h2>
              <p className="text-gray-400">Vedic astrology chart</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
          >
            <X size={24} className="text-gray-400" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {loading ? (
            <div className="text-center py-12">
              <Loader2 size={64} className="text-violet-400 mx-auto mb-4 animate-spin" />
              <h3 className="text-xl font-bold text-white mb-2">Loading Birth Chart</h3>
              <p className="text-gray-400">Calculating planetary positions...</p>
            </div>
          ) : error ? (
            <div className="text-center py-12">
              <User size={64} className="text-red-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">Error Loading Chart</h3>
              <p className="text-red-400 mb-4">{error}</p>
              <button
                onClick={fetchBirthChart}
                className="px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700 transition-colors"
              >
                Retry
              </button>
            </div>
          ) : chartData ? (
            <div className="space-y-6">
              {/* Birth Data */}
              <div className="bg-slate-800 rounded-lg p-4">
                <h4 className="text-white font-semibold mb-3">Birth Information</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                  <div>
                    <span className="text-gray-400">Name:</span>
                    <span className="text-white ml-2">{chartData.birth_data?.name || 'N/A'}</span>
                  </div>
                  <div>
                    <span className="text-gray-400">Birth Date:</span>
                    <span className="text-white ml-2">{chartData.birth_data?.birth_date || 'N/A'}</span>
                  </div>
                  <div>
                    <span className="text-gray-400">Birth Time:</span>
                    <span className="text-white ml-2">{chartData.birth_data?.birth_time || 'N/A'}</span>
                  </div>
                  <div>
                    <span className="text-gray-400">Birth Place:</span>
                    <span className="text-white ml-2">{chartData.birth_data?.birth_place || 'N/A'}</span>
                  </div>
                </div>
              </div>

              {/* Chart Summary */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-slate-800 rounded-lg p-4 text-center">
                  <h5 className="text-white font-semibold mb-2">Ascendant</h5>
                  <p className="text-violet-400 text-lg">{chartData.ascendant || 'N/A'}</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-4 text-center">
                  <h5 className="text-white font-semibold mb-2">Sun Sign</h5>
                  <p className="text-yellow-400 text-lg">{chartData.sun_sign || 'N/A'}</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-4 text-center">
                  <h5 className="text-white font-semibold mb-2">Moon Sign</h5>
                  <p className="text-blue-400 text-lg">{chartData.moon_sign || 'N/A'}</p>
                </div>
              </div>

              {/* Planetary Positions */}
              {chartData.planetary_positions && chartData.planetary_positions.length > 0 && (
                <div className="bg-slate-800 rounded-lg p-4">
                  <h4 className="text-white font-semibold mb-3">Planetary Positions</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                    {chartData.planetary_positions.map((planet, index) => (
                      <div key={index} className="bg-slate-700 rounded p-3">
                        <div className="flex justify-between items-center mb-1">
                          <span className="text-white font-medium">{planet.planet}</span>
                          <span className="text-gray-400 text-sm">H{planet.house}</span>
                        </div>
                        <div className="text-sm">
                          <div className="text-violet-400">{planet.sign}</div>
                          <div className="text-gray-400">{planet.degree}°</div>
                          <div className="text-purple-400">{planet.nakshatra}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-12">
              <User size={64} className="text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">No Profile Available</h3>
              <p className="text-gray-400 mb-6">Please create a profile first to view your birth chart</p>
              <button
                onClick={onClose}
                className="px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700 transition-colors"
              >
                Close
              </button>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
