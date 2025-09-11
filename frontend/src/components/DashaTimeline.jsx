// frontend/src/components/DashaTimeline.jsx
import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

const DashaTimeline = ({ profile, chartId }) => {
  const { t } = useTranslation();
  const [dashaData, setDashaData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedPeriod, setSelectedPeriod] = useState(null);

  useEffect(() => {
    if (profile || chartId) {
      fetchDashaData();
    }
  }, [profile, chartId]);

  const fetchDashaData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      let url;
      if (chartId) {
        url = `/api/dasha/${chartId}`;
      } else if (profile) {
        // Calculate dasha for profile
        url = '/api/dasha/calculate';
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            birth_date: profile.birth_date,
            birth_time: profile.birth_time,
            latitude: profile.latitude,
            longitude: profile.longitude,
            timezone: profile.timezone
          }),
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        setDashaData(data);
        return;
      }
      
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setDashaData(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching dasha data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getPlanetColor = (planet) => {
    const colors = {
      'Sun': 'bg-yellow-100 text-yellow-800 border-yellow-200',
      'Moon': 'bg-blue-100 text-blue-800 border-blue-200',
      'Mars': 'bg-red-100 text-red-800 border-red-200',
      'Mercury': 'bg-green-100 text-green-800 border-green-200',
      'Jupiter': 'bg-purple-100 text-purple-800 border-purple-200',
      'Venus': 'bg-pink-100 text-pink-800 border-pink-200',
      'Saturn': 'bg-gray-100 text-gray-800 border-gray-200',
      'Rahu': 'bg-orange-100 text-orange-800 border-orange-200',
      'Ketu': 'bg-indigo-100 text-indigo-800 border-indigo-200'
    };
    return colors[planet] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const calculateProgress = (startDate, endDate) => {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const now = new Date();
    
    if (now < start) return 0;
    if (now > end) return 100;
    
    const total = end - start;
    const elapsed = now - start;
    return Math.round((elapsed / total) * 100);
  };

  const getProgressColor = (progress) => {
    if (progress < 25) return 'bg-red-500';
    if (progress < 50) return 'bg-orange-500';
    if (progress < 75) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  if (loading) {
    return (
      <div className="dasha-timeline bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">{t('loading_dasha')}</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dasha-timeline bg-white rounded-lg shadow-md p-6">
        <div className="text-red-600 text-center">
          <p>{t('error_loading_dasha')}</p>
          <p className="text-sm text-gray-500">{error}</p>
          <button 
            onClick={fetchDashaData}
            className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            {t('retry')}
          </button>
        </div>
      </div>
    );
  }

  if (!dashaData) {
    return (
      <div className="dasha-timeline bg-white rounded-lg shadow-md p-6">
        <div className="text-center text-gray-500">
          <p>{t('no_dasha_data')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dasha-timeline bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">{t('dasha_timeline')}</h2>
        <button 
          onClick={fetchDashaData}
          className="text-blue-600 hover:text-blue-800"
        >
          {t('refresh')}
        </button>
      </div>

      {/* Current Dasha */}
      {dashaData.current_dasha && (
        <div className="bg-blue-50 p-4 rounded-lg mb-6">
          <h3 className="font-semibold text-blue-800 mb-3">{t('current_dasha')}</h3>
          <div className="flex items-center justify-between">
            <div>
              <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium border ${getPlanetColor(dashaData.current_dasha.planet)}`}>
                {dashaData.current_dasha.planet}
              </div>
              <p className="text-sm text-gray-600 mt-1">
                {formatDate(dashaData.current_dasha.start_date)} - {formatDate(dashaData.current_dasha.end_date)}
              </p>
              <p className="text-sm text-gray-600">
                {t('duration')}: {dashaData.current_dasha.duration_years} {t('years')}
              </p>
            </div>
            <div className="text-right">
              <div className="w-32 bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full ${getProgressColor(calculateProgress(dashaData.current_dasha.start_date, dashaData.current_dasha.end_date))}`}
                  style={{ width: `${calculateProgress(dashaData.current_dasha.start_date, dashaData.current_dasha.end_date)}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                {calculateProgress(dashaData.current_dasha.start_date, dashaData.current_dasha.end_date)}% {t('complete')}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Current Antardasha */}
      {dashaData.current_antardasha && (
        <div className="bg-green-50 p-4 rounded-lg mb-6">
          <h3 className="font-semibold text-green-800 mb-3">{t('current_antardasha')}</h3>
          <div className="flex items-center justify-between">
            <div>
              <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium border ${getPlanetColor(dashaData.current_antardasha.planet)}`}>
                {dashaData.current_antardasha.planet}
              </div>
              <p className="text-sm text-gray-600 mt-1">
                {formatDate(dashaData.current_antardasha.start_date)} - {formatDate(dashaData.current_antardasha.end_date)}
              </p>
              <p className="text-sm text-gray-600">
                {t('duration')}: {dashaData.current_antardasha.duration_days} {t('days')}
              </p>
            </div>
            <div className="text-right">
              <div className="w-32 bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full ${getProgressColor(calculateProgress(dashaData.current_antardasha.start_date, dashaData.current_antardasha.end_date))}`}
                  style={{ width: `${calculateProgress(dashaData.current_antardasha.start_date, dashaData.current_antardasha.end_date)}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                {calculateProgress(dashaData.current_antardasha.start_date, dashaData.current_antardasha.end_date)}% {t('complete')}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Upcoming Dasha Periods */}
      {dashaData.upcoming_periods && dashaData.upcoming_periods.length > 0 && (
        <div className="mb-6">
          <h3 className="font-semibold text-gray-800 mb-4">{t('upcoming_dasha_periods')}</h3>
          <div className="space-y-3">
            {dashaData.upcoming_periods.map((period, index) => (
              <div
                key={index}
                className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                  selectedPeriod?.planet === period.planet && selectedPeriod?.start_date === period.start_date
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => setSelectedPeriod(period)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`px-3 py-1 rounded-full text-sm font-medium border ${getPlanetColor(period.planet)}`}>
                      {period.planet}
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">
                        {formatDate(period.start_date)} - {formatDate(period.end_date)}
                      </p>
                      <p className="text-sm text-gray-600">
                        {t('duration')}: {period.duration_years} {t('years')}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-500">
                      {t('starts_in')}: {Math.ceil((new Date(period.start_date) - new Date()) / (1000 * 60 * 60 * 24))} {t('days')}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Antardasha Sequence */}
      {dashaData.antardasha_sequence && dashaData.antardasha_sequence.length > 0 && (
        <div className="mb-6">
          <h3 className="font-semibold text-gray-800 mb-4">{t('antardasha_sequence')}</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {dashaData.antardasha_sequence.map((antardasha, index) => (
              <div
                key={index}
                className={`border rounded-lg p-3 cursor-pointer transition-colors ${
                  antardasha.is_active
                    ? 'border-green-500 bg-green-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => setSelectedPeriod(antardasha)}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className={`px-2 py-1 rounded-full text-xs font-medium border ${getPlanetColor(antardasha.planet)}`}>
                    {antardasha.planet}
                  </div>
                  {antardasha.is_active && (
                    <span className="text-xs text-green-600 font-medium">{t('active')}</span>
                  )}
                </div>
                <div className="text-xs text-gray-600">
                  <p>{formatDate(antardasha.start_date)} - {formatDate(antardasha.end_date)}</p>
                  <p>{t('duration')}: {antardasha.duration_days} {t('days')}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Selected Period Details */}
      {selectedPeriod && (
        <div className="bg-gray-50 p-4 rounded-lg mb-6">
          <h3 className="font-semibold text-gray-800 mb-3">
            {t('period_details')} - {selectedPeriod.planet}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-600">{t('start_date')}:</span>
              <p className="text-gray-800">{formatDate(selectedPeriod.start_date)}</p>
            </div>
            <div>
              <span className="font-medium text-gray-600">{t('end_date')}:</span>
              <p className="text-gray-800">{formatDate(selectedPeriod.end_date)}</p>
            </div>
            <div>
              <span className="font-medium text-gray-600">{t('duration')}:</span>
              <p className="text-gray-800">
                {selectedPeriod.duration_years ? `${selectedPeriod.duration_years} ${t('years')}` : `${selectedPeriod.duration_days} ${t('days')}`}
              </p>
            </div>
            <div>
              <span className="font-medium text-gray-600">{t('status')}:</span>
              <p className="text-gray-800">
                {selectedPeriod.is_active ? t('active') : t('upcoming')}
              </p>
            </div>
          </div>
          <div className="mt-3">
            <p className="text-sm text-gray-600">
              {/* TODO: Add detailed interpretation based on planet and period */}
              {t('period_interpretation_placeholder')}
            </p>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex gap-4">
        <button
          onClick={() => {
            // TODO: Generate predictions
            console.log('Generate predictions for dasha:', dashaData);
          }}
          className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
        >
          {t('generate_predictions')}
        </button>
        <button
          onClick={() => {
            // TODO: Save dasha timeline
            console.log('Save dasha timeline:', dashaData);
          }}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          {t('save_timeline')}
        </button>
        <button
          onClick={() => {
            // TODO: Export dasha
            console.log('Export dasha:', dashaData);
          }}
          className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
        >
          {t('export_dasha')}
        </button>
      </div>
    </div>
  );
};

export default DashaTimeline;
