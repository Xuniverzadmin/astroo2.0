// frontend/src/components/PanchangamWidget.jsx
import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

const PanchangamWidget = ({ date, location, onDateChange, onLocationChange }) => {
  const { t } = useTranslation();
  const [panchangamData, setPanchangamData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (date && location) {
      fetchPanchangamData();
    }
  }, [date, location]);

  const fetchPanchangamData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(
        `/api/panchangam/${date}?lat=${location.latitude}&lon=${location.longitude}&tz=${location.timezone}`
      );
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setPanchangamData(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching panchangam data:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (timeString) => {
    if (!timeString) return '--';
    return new Date(timeString).toLocaleTimeString();
  };

  if (loading) {
    return (
      <div className="panchangam-widget bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">{t('loading')}</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="panchangam-widget bg-white rounded-lg shadow-md p-6">
        <div className="text-red-600 text-center">
          <p>{t('error_loading_panchangam')}</p>
          <p className="text-sm text-gray-500">{error}</p>
          <button 
            onClick={fetchPanchangamData}
            className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            {t('retry')}
          </button>
        </div>
      </div>
    );
  }

  if (!panchangamData) {
    return (
      <div className="panchangam-widget bg-white rounded-lg shadow-md p-6">
        <div className="text-center text-gray-500">
          <p>{t('no_panchangam_data')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="panchangam-widget bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-semibold text-gray-800">
          {t('panchangam_for')} {new Date(panchangamData.date).toLocaleDateString()}
        </h3>
        <button 
          onClick={fetchPanchangamData}
          className="text-blue-600 hover:text-blue-800"
        >
          {t('refresh')}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Sunrise/Sunset */}
        <div className="bg-yellow-50 p-4 rounded-lg">
          <h4 className="font-medium text-yellow-800 mb-2">{t('sun_times')}</h4>
          <div className="space-y-1 text-sm">
            <div className="flex justify-between">
              <span>{t('sunrise')}:</span>
              <span className="font-medium">{formatTime(panchangamData.sunrise)}</span>
            </div>
            <div className="flex justify-between">
              <span>{t('sunset')}:</span>
              <span className="font-medium">{formatTime(panchangamData.sunset)}</span>
            </div>
          </div>
        </div>

        {/* Tithi */}
        <div className="bg-blue-50 p-4 rounded-lg">
          <h4 className="font-medium text-blue-800 mb-2">{t('tithi')}</h4>
          <div className="space-y-1 text-sm">
            <div className="font-medium">{panchangamData.tithi?.name}</div>
            <div className="text-gray-600">
              {t('progress')}: {panchangamData.tithi?.percentage}%
            </div>
          </div>
        </div>

        {/* Nakshatra */}
        <div className="bg-green-50 p-4 rounded-lg">
          <h4 className="font-medium text-green-800 mb-2">{t('nakshatra')}</h4>
          <div className="space-y-1 text-sm">
            <div className="font-medium">{panchangamData.nakshatra?.name}</div>
            <div className="text-gray-600">
              {t('progress')}: {panchangamData.nakshatra?.percentage}%
            </div>
          </div>
        </div>

        {/* Yoga */}
        <div className="bg-purple-50 p-4 rounded-lg">
          <h4 className="font-medium text-purple-800 mb-2">{t('yoga')}</h4>
          <div className="space-y-1 text-sm">
            <div className="font-medium">{panchangamData.yoga?.name}</div>
            <div className="text-gray-600">
              {t('progress')}: {panchangamData.yoga?.percentage}%
            </div>
          </div>
        </div>

        {/* Karana */}
        <div className="bg-orange-50 p-4 rounded-lg">
          <h4 className="font-medium text-orange-800 mb-2">{t('karana')}</h4>
          <div className="space-y-1 text-sm">
            <div className="font-medium">{panchangamData.karana?.name}</div>
            <div className="text-gray-600">
              {t('progress')}: {panchangamData.karana?.percentage}%
            </div>
          </div>
        </div>

        {/* Rahu Kalam */}
        <div className="bg-red-50 p-4 rounded-lg">
          <h4 className="font-medium text-red-800 mb-2">{t('rahu_kalam')}</h4>
          <div className="space-y-1 text-sm">
            <div className="text-gray-600">
              {panchangamData.rahu_kalam || t('not_available')}
            </div>
          </div>
        </div>
      </div>

      {/* Location Info */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <div className="text-sm text-gray-600">
          <span className="font-medium">{t('location')}:</span> {location.latitude}, {location.longitude}
          <span className="ml-2">({location.timezone})</span>
        </div>
      </div>
    </div>
  );
};

export default PanchangamWidget;
