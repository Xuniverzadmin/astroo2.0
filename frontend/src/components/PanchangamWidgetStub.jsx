// Real PanchangamWidget that calls the backend API
import { motion } from 'framer-motion';
import { Calendar, Clock, Loader2, MapPin, Moon, Sun, X } from 'lucide-react';
import React, { useEffect, useState } from 'react';
import { apiJSON } from '../api';

export default function PanchangamWidgetStub({ data, onClose }) {
  const [panchangamData, setPanchangamData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPanchangamData();
  }, []);

  const fetchPanchangamData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Use today's date or the date from data prop
      const date = data?.date || new Date().toISOString().split('T')[0];

      // Default to Chennai coordinates if not provided
      const lat = data?.lat || 13.0827;
      const lon = data?.lon || 80.2707;
      const tz = data?.tz || 'Asia/Kolkata';

      const result = await apiJSON(`/api/panchangam/${date}?lat=${lat}&lon=${lon}&tz=${tz}`);
      console.log('Panchangam API response:', result);
      console.log('Rahu Kalam type:', typeof result.rahu_kalam, result.rahu_kalam);
      console.log('Yama Gandam type:', typeof result.yama_gandam, result.yama_gandam);
      console.log('Gulikai Kalam type:', typeof result.gulikai_kalam, result.gulikai_kalam);
      setPanchangamData(result);
    } catch (err) {
      console.error('Error fetching panchangam data:', err);
      setError(err.message || 'Failed to load panchangam data');
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
            <div className="p-2 rounded-lg bg-indigo-600">
              <Calendar size={24} className="text-white" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">Today's Panchangam</h2>
              <p className="text-gray-400">Vedic calendar information</p>
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
              <Loader2 size={64} className="text-indigo-400 mx-auto mb-4 animate-spin" />
              <h3 className="text-xl font-bold text-white mb-2">Loading Panchangam</h3>
              <p className="text-gray-400">Fetching Vedic calendar data...</p>
            </div>
          ) : error ? (
            <div className="text-center py-12">
              <Calendar size={64} className="text-red-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">Error Loading Data</h3>
              <p className="text-red-400 mb-4">{error}</p>
              <button
                onClick={fetchPanchangamData}
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
              >
                Retry
              </button>
            </div>
          ) : panchangamData ? (
            <div className="space-y-6">
              {/* Date and Location */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Calendar className="text-indigo-400" size={20} />
                  <span className="text-white font-semibold">{panchangamData.date}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-400">
                  <MapPin size={16} />
                  <span className="text-sm">Lat: {panchangamData.location?.latitude}, Lon: {panchangamData.location?.longitude}</span>
                </div>
              </div>

              {/* Sun Times */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-slate-800 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Sun className="text-yellow-400" size={20} />
                    <span className="text-white font-semibold">Sunrise</span>
                  </div>
                  <p className="text-gray-300">{panchangamData.sunrise || 'N/A'}</p>
                </div>
                <div className="bg-slate-800 rounded-lg p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Moon className="text-blue-400" size={20} />
                    <span className="text-white font-semibold">Sunset</span>
                  </div>
                  <p className="text-gray-300">{panchangamData.sunset || 'N/A'}</p>
                </div>
              </div>

              {/* Panchangam Elements */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Tithi */}
                <div className="bg-slate-800 rounded-lg p-4">
                  <h4 className="text-white font-semibold mb-2">Tithi</h4>
                  <p className="text-indigo-400 font-medium">{panchangamData.tithi?.name || 'N/A'}</p>
                  <p className="text-gray-400 text-sm">Progress: {panchangamData.tithi?.percentage || 0}%</p>
                </div>

                {/* Nakshatra */}
                <div className="bg-slate-800 rounded-lg p-4">
                  <h4 className="text-white font-semibold mb-2">Nakshatra</h4>
                  <p className="text-purple-400 font-medium">{panchangamData.nakshatra?.name || 'N/A'}</p>
                  <p className="text-gray-400 text-sm">Progress: {panchangamData.nakshatra?.percentage || 0}%</p>
                </div>

                {/* Yoga */}
                <div className="bg-slate-800 rounded-lg p-4">
                  <h4 className="text-white font-semibold mb-2">Yoga</h4>
                  <p className="text-green-400 font-medium">{panchangamData.yoga?.name || 'N/A'}</p>
                  <p className="text-gray-400 text-sm">Progress: {panchangamData.yoga?.percentage || 0}%</p>
                </div>

                {/* Karana */}
                <div className="bg-slate-800 rounded-lg p-4">
                  <h4 className="text-white font-semibold mb-2">Karana</h4>
                  <p className="text-orange-400 font-medium">{panchangamData.karana?.name || 'N/A'}</p>
                  <p className="text-gray-400 text-sm">Progress: {panchangamData.karana?.percentage || 0}%</p>
                </div>
              </div>

              {/* Auspicious Times */}
              <div className="bg-slate-800 rounded-lg p-4">
                <h4 className="text-white font-semibold mb-3 flex items-center gap-2">
                  <Clock className="text-yellow-400" size={20} />
                  Auspicious Times
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  <div className="text-center">
                    <p className="text-red-400 font-medium">Rahu Kalam</p>
                    <p className="text-gray-300 text-sm">
                      {(() => {
                        const rahu = panchangamData.rahu_kalam;
                        if (!rahu) return 'N/A';
                        if (typeof rahu === 'string') return rahu;
                        if (typeof rahu === 'object' && rahu.start && rahu.end) {
                          return `${rahu.start} - ${rahu.end}`;
                        }
                        return JSON.stringify(rahu);
                      })()}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-yellow-400 font-medium">Yama Gandam</p>
                    <p className="text-gray-300 text-sm">
                      {(() => {
                        const yama = panchangamData.yama_gandam;
                        if (!yama) return 'N/A';
                        if (typeof yama === 'string') return yama;
                        if (typeof yama === 'object' && yama.start && yama.end) {
                          return `${yama.start} - ${yama.end}`;
                        }
                        return JSON.stringify(yama);
                      })()}
                    </p>
                  </div>
                  <div className="text-center">
                    <p className="text-orange-400 font-medium">Gulikai Kalam</p>
                    <p className="text-gray-300 text-sm">
                      {(() => {
                        const gulikai = panchangamData.gulikai_kalam;
                        if (!gulikai) return 'N/A';
                        if (typeof gulikai === 'string') return gulikai;
                        if (typeof gulikai === 'object' && gulikai.start && gulikai.end) {
                          return `${gulikai.start} - ${gulikai.end}`;
                        }
                        return JSON.stringify(gulikai);
                      })()}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-12">
              <Calendar size={64} className="text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">No Data Available</h3>
              <p className="text-gray-400">Unable to load panchangam data</p>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
