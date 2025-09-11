// frontend/src/components/ReadingSummary.jsx
import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

const ReadingSummary = ({ chartId, readingType = 'general', onGenerateNew }) => {
  const { t } = useTranslation();
  const [readingData, setReadingData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedSection, setSelectedSection] = useState('summary');

  useEffect(() => {
    if (chartId) {
      fetchReadingData();
    }
  }, [chartId, readingType]);

  const fetchReadingData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`/api/interpretation/generate?chart_id=${chartId}&interpretation_type=${readingType}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setReadingData(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching reading data:', err);
    } finally {
      setLoading(false);
    }
  };

  const generatePrediction = async (timePeriod, focusArea) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/predictions/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          chart_id: chartId,
          prediction_type: 'short_term',
          time_period: timePeriod,
          focus_area: focusArea,
          include_remedies: true
        }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (err) {
      setError(err.message);
      console.error('Error generating prediction:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return (
      <div className="reading-summary bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">{t('generating_reading')}</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="reading-summary bg-white rounded-lg shadow-md p-6">
        <div className="text-red-600 text-center">
          <p>{t('error_generating_reading')}</p>
          <p className="text-sm text-gray-500">{error}</p>
          <button 
            onClick={fetchReadingData}
            className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            {t('retry')}
          </button>
        </div>
      </div>
    );
  }

  if (!readingData) {
    return (
      <div className="reading-summary bg-white rounded-lg shadow-md p-6">
        <div className="text-center text-gray-500">
          <p>{t('no_reading_data')}</p>
          {onGenerateNew && (
            <button
              onClick={onGenerateNew}
              className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              {t('generate_reading')}
            </button>
          )}
        </div>
      </div>
    );
  }

  const sections = [
    { id: 'summary', label: t('summary'), icon: '📋' },
    { id: 'strengths', label: t('strengths'), icon: '💪' },
    { id: 'challenges', label: t('challenges'), icon: '⚠️' },
    { id: 'recommendations', label: t('recommendations'), icon: '💡' },
    { id: 'predictions', label: t('predictions'), icon: '🔮' }
  ];

  return (
    <div className="reading-summary bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">
          {t('reading_summary')} - {t(readingType)}
        </h2>
        <div className="flex gap-2">
          <button 
            onClick={fetchReadingData}
            className="text-blue-600 hover:text-blue-800"
          >
            {t('refresh')}
          </button>
          {onGenerateNew && (
            <button
              onClick={onGenerateNew}
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            >
              {t('generate_new')}
            </button>
          )}
        </div>
      </div>

      {/* Reading Metadata */}
      <div className="bg-gray-50 p-4 rounded-lg mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <span className="font-medium text-gray-600">{t('generated_at')}:</span>
            <p className="text-gray-800">{formatDate(readingData.generated_at)}</p>
          </div>
          <div>
            <span className="font-medium text-gray-600">{t('reading_type')}:</span>
            <p className="text-gray-800">{t(readingData.interpretation_type)}</p>
          </div>
          <div>
            <span className="font-medium text-gray-600">{t('language')}:</span>
            <p className="text-gray-800">{readingData.language}</p>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          {sections.map((section) => (
            <button
              key={section.id}
              onClick={() => setSelectedSection(section.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                selectedSection === section.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <span className="mr-2">{section.icon}</span>
              {section.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Content Sections */}
      <div className="min-h-96">
        {selectedSection === 'summary' && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">{t('overview')}</h3>
            <p className="text-gray-700 leading-relaxed">{readingData.summary}</p>
            
            <h3 className="text-lg font-semibold text-gray-800 mt-6">{t('detailed_analysis')}</h3>
            <p className="text-gray-700 leading-relaxed">{readingData.detailed_analysis}</p>
          </div>
        )}

        {selectedSection === 'strengths' && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">{t('your_strengths')}</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {readingData.strengths?.map((strength, index) => (
                <div key={index} className="bg-green-50 p-4 rounded-lg border border-green-200">
                  <div className="flex items-start">
                    <span className="text-green-600 mr-2">✓</span>
                    <p className="text-green-800">{strength}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {selectedSection === 'challenges' && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">{t('areas_for_growth')}</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {readingData.challenges?.map((challenge, index) => (
                <div key={index} className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
                  <div className="flex items-start">
                    <span className="text-yellow-600 mr-2">⚠</span>
                    <p className="text-yellow-800">{challenge}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {selectedSection === 'recommendations' && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">{t('recommendations')}</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {readingData.recommendations?.map((recommendation, index) => (
                <div key={index} className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                  <div className="flex items-start">
                    <span className="text-blue-600 mr-2">💡</span>
                    <p className="text-blue-800">{recommendation}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {selectedSection === 'predictions' && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-800">{t('predictions')}</h3>
            <div className="space-y-3">
              {readingData.predictions?.map((prediction, index) => (
                <div key={index} className="bg-purple-50 p-4 rounded-lg border border-purple-200">
                  <div className="flex items-start">
                    <span className="text-purple-600 mr-2">🔮</span>
                    <p className="text-purple-800">{prediction}</p>
                  </div>
                </div>
              ))}
            </div>
            
            {/* Generate More Predictions */}
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <h4 className="font-medium text-gray-800 mb-3">{t('generate_more_predictions')}</h4>
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => generatePrediction('1_month', 'career')}
                  className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
                >
                  {t('career_1_month')}
                </button>
                <button
                  onClick={() => generatePrediction('6_months', 'love')}
                  className="px-3 py-1 bg-pink-600 text-white text-sm rounded hover:bg-pink-700"
                >
                  {t('love_6_months')}
                </button>
                <button
                  onClick={() => generatePrediction('1_year', 'health')}
                  className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700"
                >
                  {t('health_1_year')}
                </button>
                <button
                  onClick={() => generatePrediction('5_years', 'finance')}
                  className="px-3 py-1 bg-yellow-600 text-white text-sm rounded hover:bg-yellow-700"
                >
                  {t('finance_5_years')}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="mt-6 pt-6 border-t border-gray-200 flex gap-4">
        <button
          onClick={() => {
            // TODO: Save reading
            console.log('Save reading:', readingData);
          }}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          {t('save_reading')}
        </button>
        <button
          onClick={() => {
            // TODO: Share reading
            console.log('Share reading:', readingData);
          }}
          className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
        >
          {t('share_reading')}
        </button>
        <button
          onClick={() => {
            // TODO: Export reading
            console.log('Export reading:', readingData);
          }}
          className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
        >
          {t('export_reading')}
        </button>
      </div>
    </div>
  );
};

export default ReadingSummary;
