// frontend/src/components/BirthChartView.jsx
import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

const BirthChartView = ({ profile, chartId }) => {
  const { t } = useTranslation();
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedPlanet, setSelectedPlanet] = useState(null);

  useEffect(() => {
    if (profile || chartId) {
      fetchChartData();
    }
  }, [profile, chartId]);

  const fetchChartData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      let url;
      if (chartId) {
        url = `/api/birth-chart/${chartId}`;
      } else if (profile) {
        // Calculate chart for profile
        url = '/api/birth-chart/calculate';
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: profile.name,
            birth_date: profile.birth_date,
            birth_time: profile.birth_time,
            birth_place: profile.birth_place,
            latitude: profile.latitude,
            longitude: profile.longitude,
            timezone: profile.timezone
          }),
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        setChartData(data);
        return;
      }
      
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setChartData(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching chart data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getPlanetColor = (planet) => {
    const colors = {
      'Sun': 'text-yellow-600',
      'Moon': 'text-blue-600',
      'Mars': 'text-red-600',
      'Mercury': 'text-green-600',
      'Jupiter': 'text-purple-600',
      'Venus': 'text-pink-600',
      'Saturn': 'text-gray-600',
      'Rahu': 'text-orange-600',
      'Ketu': 'text-indigo-600'
    };
    return colors[planet] || 'text-gray-600';
  };

  const getSignColor = (sign) => {
    const colors = {
      'Aries': 'bg-red-100 text-red-800',
      'Taurus': 'bg-green-100 text-green-800',
      'Gemini': 'bg-yellow-100 text-yellow-800',
      'Cancer': 'bg-blue-100 text-blue-800',
      'Leo': 'bg-orange-100 text-orange-800',
      'Virgo': 'bg-gray-100 text-gray-800',
      'Libra': 'bg-pink-100 text-pink-800',
      'Scorpio': 'bg-red-100 text-red-800',
      'Sagittarius': 'bg-purple-100 text-purple-800',
      'Capricorn': 'bg-gray-100 text-gray-800',
      'Aquarius': 'bg-blue-100 text-blue-800',
      'Pisces': 'bg-indigo-100 text-indigo-800'
    };
    return colors[sign] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="birth-chart-view bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">{t('loading_chart')}</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="birth-chart-view bg-white rounded-lg shadow-md p-6">
        <div className="text-red-600 text-center">
          <p>{t('error_loading_chart')}</p>
          <p className="text-sm text-gray-500">{error}</p>
          <button 
            onClick={fetchChartData}
            className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            {t('retry')}
          </button>
        </div>
      </div>
    );
  }

  if (!chartData) {
    return (
      <div className="birth-chart-view bg-white rounded-lg shadow-md p-6">
        <div className="text-center text-gray-500">
          <p>{t('no_chart_data')}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="birth-chart-view bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">
          {t('birth_chart')} - {chartData.birth_data?.name || t('unknown')}
        </h2>
        <button 
          onClick={fetchChartData}
          className="text-blue-600 hover:text-blue-800"
        >
          {t('refresh')}
        </button>
      </div>

      {/* Birth Data Summary */}
      <div className="bg-gray-50 p-4 rounded-lg mb-6">
        <h3 className="font-semibold text-gray-800 mb-3">{t('birth_information')}</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
          <div>
            <span className="font-medium text-gray-600">{t('birth_date')}:</span>
            <p className="text-gray-800">{new Date(chartData.birth_data?.date).toLocaleDateString()}</p>
          </div>
          <div>
            <span className="font-medium text-gray-600">{t('birth_time')}:</span>
            <p className="text-gray-800">{chartData.birth_data?.time}</p>
          </div>
          <div>
            <span className="font-medium text-gray-600">{t('ascendant')}:</span>
            <p className="text-gray-800">{chartData.ascendant?.sign}</p>
          </div>
          <div>
            <span className="font-medium text-gray-600">{t('moon_sign')}:</span>
            <p className="text-gray-800">{chartData.moon_sign}</p>
          </div>
        </div>
      </div>

      {/* Planetary Positions */}
      <div className="mb-6">
        <h3 className="font-semibold text-gray-800 mb-4">{t('planetary_positions')}</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {chartData.planetary_positions?.map((planet) => (
            <div
              key={planet.planet}
              className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                selectedPlanet?.planet === planet.planet
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => setSelectedPlanet(planet)}
            >
              <div className="flex justify-between items-start mb-2">
                <h4 className={`font-semibold ${getPlanetColor(planet.planet)}`}>
                  {planet.planet}
                </h4>
                <span className={`px-2 py-1 rounded-full text-xs ${getSignColor(planet.sign)}`}>
                  {planet.sign}
                </span>
              </div>
              
              <div className="space-y-1 text-sm text-gray-600">
                <div>
                  <span className="font-medium">{t('degree')}:</span> {planet.degree}°
                </div>
                <div>
                  <span className="font-medium">{t('house')}:</span> {planet.house}
                </div>
                <div>
                  <span className="font-medium">{t('nakshatra')}:</span> {planet.nakshatra}
                </div>
                <div>
                  <span className="font-medium">{t('nakshatra_lord')}:</span> {planet.nakshatra_lord}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Selected Planet Details */}
      {selectedPlanet && (
        <div className="bg-blue-50 p-4 rounded-lg mb-6">
          <h3 className="font-semibold text-gray-800 mb-3">
            {t('detailed_analysis')} - {selectedPlanet.planet}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-600">{t('position')}:</span>
              <p className="text-gray-800">
                {selectedPlanet.degree}° {selectedPlanet.sign} ({t('house')} {selectedPlanet.house})
              </p>
            </div>
            <div>
              <span className="font-medium text-gray-600">{t('nakshatra')}:</span>
              <p className="text-gray-800">
                {selectedPlanet.nakshatra} ({selectedPlanet.nakshatra_lord})
              </p>
            </div>
          </div>
          <div className="mt-3">
            <p className="text-sm text-gray-600">
              {/* TODO: Add detailed interpretation based on planet position */}
              {t('detailed_interpretation_placeholder')}
            </p>
          </div>
        </div>
      )}

      {/* Houses */}
      {chartData.houses && (
        <div className="mb-6">
          <h3 className="font-semibold text-gray-800 mb-4">{t('houses')}</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {chartData.houses.map((house) => (
              <div key={house.house} className="border border-gray-200 rounded-lg p-3">
                <div className="flex justify-between items-center mb-2">
                  <h4 className="font-medium text-gray-800">{t('house')} {house.house}</h4>
                  <span className={`px-2 py-1 rounded-full text-xs ${getSignColor(house.sign)}`}>
                    {house.sign}
                  </span>
                </div>
                <div className="text-sm text-gray-600">
                  <span className="font-medium">{t('degree')}:</span> {house.degree}°
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex gap-4">
        <button
          onClick={() => {
            // TODO: Generate interpretation
            console.log('Generate interpretation for chart:', chartData);
          }}
          className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
        >
          {t('generate_interpretation')}
        </button>
        <button
          onClick={() => {
            // TODO: Save chart
            console.log('Save chart:', chartData);
          }}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          {t('save_chart')}
        </button>
        <button
          onClick={() => {
            // TODO: Export chart
            console.log('Export chart:', chartData);
          }}
          className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
        >
          {t('export_chart')}
        </button>
      </div>
    </div>
  );
};

export default BirthChartView;
