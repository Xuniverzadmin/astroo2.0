// frontend/src/components/PersonalizationBar.jsx
import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

const PersonalizationBar = ({ userId, onPreferencesChange }) => {
  const { t, i18n } = useTranslation();
  const [preferences, setPreferences] = useState({
    language: 'en',
    timezone: 'Asia/Kolkata',
    calculation_method: 'Lahiri',
    chart_style: 'North Indian',
    show_degrees: true,
    show_nakshatras: true,
    show_divisions: false,
    notification_enabled: true,
    email_notifications: true,
    sms_notifications: false
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isExpanded, setIsExpanded] = useState(false);

  useEffect(() => {
    fetchUserPreferences();
  }, [userId]);

  const fetchUserPreferences = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // TODO: Implement actual API call to fetch user preferences
      // const response = await fetch(`/api/user/${userId}/preferences`);
      // const data = await response.json();
      // setPreferences(data.preferences);
      
      // For now, use default preferences
      console.log('Fetching preferences for user:', userId);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching preferences:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePreferenceChange = (key, value) => {
    const newPreferences = {
      ...preferences,
      [key]: value
    };
    setPreferences(newPreferences);
    
    // Update language immediately if changed
    if (key === 'language' && value !== i18n.language) {
      i18n.changeLanguage(value);
    }
    
    // Notify parent component
    if (onPreferencesChange) {
      onPreferencesChange(newPreferences);
    }
  };

  const savePreferences = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // TODO: Implement actual API call to save preferences
      // const response = await fetch(`/api/user/${userId}/preferences`, {
      //   method: 'PUT',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify({ preferences }),
      // });
      
      console.log('Saving preferences:', preferences);
      
      // Show success message
      // TODO: Add toast notification
    } catch (err) {
      setError(err.message);
      console.error('Error saving preferences:', err);
    } finally {
      setLoading(false);
    }
  };

  const supportedLanguages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'Hindi' },
    { code: 'ta', name: 'Tamil' },
    { code: 'te', name: 'Telugu' },
    { code: 'kn', name: 'Kannada' },
    { code: 'ml', name: 'Malayalam' },
    { code: 'bn', name: 'Bengali' },
    { code: 'gu', name: 'Gujarati' },
    { code: 'mr', name: 'Marathi' },
    { code: 'pa', name: 'Punjabi' }
  ];

  const timezones = [
    { value: 'Asia/Kolkata', label: 'Asia/Kolkata (IST)' },
    { value: 'Asia/Dubai', label: 'Asia/Dubai (GST)' },
    { value: 'America/New_York', label: 'America/New_York (EST)' },
    { value: 'Europe/London', label: 'Europe/London (GMT)' },
    { value: 'Asia/Singapore', label: 'Asia/Singapore (SGT)' },
    { value: 'Asia/Tokyo', label: 'Asia/Tokyo (JST)' },
    { value: 'Australia/Sydney', label: 'Australia/Sydney (AEST)' }
  ];

  const calculationMethods = [
    { value: 'Lahiri', label: 'Lahiri (Most Common)' },
    { value: 'Raman', label: 'Raman' },
    { value: 'KP', label: 'KP (Krishnamurti)' },
    { value: 'Fagan', label: 'Fagan-Bradley' }
  ];

  const chartStyles = [
    { value: 'North Indian', label: 'North Indian' },
    { value: 'South Indian', label: 'South Indian' },
    { value: 'East Indian', label: 'East Indian' }
  ];

  if (loading && !preferences.language) {
    return (
      <div className="personalization-bar bg-white border-b border-gray-200 p-4">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-sm text-gray-600">{t('loading_preferences')}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="personalization-bar bg-white border-b border-gray-200">
      {/* Compact View */}
      <div className="flex items-center justify-between p-4">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-gray-700">{t('language')}:</span>
            <select
              value={preferences.language}
              onChange={(e) => handlePreferenceChange('language', e.target.value)}
              className="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              {supportedLanguages.map((lang) => (
                <option key={lang.code} value={lang.code}>
                  {lang.name}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-gray-700">{t('timezone')}:</span>
            <select
              value={preferences.timezone}
              onChange={(e) => handlePreferenceChange('timezone', e.target.value)}
              className="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              {timezones.map((tz) => (
                <option key={tz.value} value={tz.value}>
                  {tz.label}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-gray-700">{t('chart_style')}:</span>
            <select
              value={preferences.chart_style}
              onChange={(e) => handlePreferenceChange('chart_style', e.target.value)}
              className="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              {chartStyles.map((style) => (
                <option key={style.value} value={style.value}>
                  {style.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            {isExpanded ? t('less_options') : t('more_options')}
          </button>
          <button
            onClick={savePreferences}
            disabled={loading}
            className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? t('saving') : t('save')}
          </button>
        </div>
      </div>

      {/* Expanded View */}
      {isExpanded && (
        <div className="border-t border-gray-200 p-4 bg-gray-50">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Calculation Settings */}
            <div>
              <h4 className="font-medium text-gray-800 mb-3">{t('calculation_settings')}</h4>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {t('ayanamsa_method')}
                  </label>
                  <select
                    value={preferences.calculation_method}
                    onChange={(e) => handlePreferenceChange('calculation_method', e.target.value)}
                    className="w-full text-sm border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-1 focus:ring-blue-500"
                  >
                    {calculationMethods.map((method) => (
                      <option key={method.value} value={method.value}>
                        {method.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* Display Settings */}
            <div>
              <h4 className="font-medium text-gray-800 mb-3">{t('display_settings')}</h4>
              <div className="space-y-3">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={preferences.show_degrees}
                    onChange={(e) => handlePreferenceChange('show_degrees', e.target.checked)}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">{t('show_degrees')}</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={preferences.show_nakshatras}
                    onChange={(e) => handlePreferenceChange('show_nakshatras', e.target.checked)}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">{t('show_nakshatras')}</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={preferences.show_divisions}
                    onChange={(e) => handlePreferenceChange('show_divisions', e.target.checked)}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">{t('show_divisions')}</span>
                </label>
              </div>
            </div>

            {/* Notification Settings */}
            <div>
              <h4 className="font-medium text-gray-800 mb-3">{t('notification_settings')}</h4>
              <div className="space-y-3">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={preferences.notification_enabled}
                    onChange={(e) => handlePreferenceChange('notification_enabled', e.target.checked)}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">{t('enable_notifications')}</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={preferences.email_notifications}
                    onChange={(e) => handlePreferenceChange('email_notifications', e.target.checked)}
                    disabled={!preferences.notification_enabled}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500 disabled:opacity-50"
                  />
                  <span className="ml-2 text-sm text-gray-700">{t('email_notifications')}</span>
                </label>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={preferences.sms_notifications}
                    onChange={(e) => handlePreferenceChange('sms_notifications', e.target.checked)}
                    disabled={!preferences.notification_enabled}
                    className="rounded border-gray-300 text-blue-600 focus:ring-blue-500 disabled:opacity-50"
                  />
                  <span className="ml-2 text-sm text-gray-700">{t('sms_notifications')}</span>
                </label>
              </div>
            </div>
          </div>

          {error && (
            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-sm text-red-600">{error}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PersonalizationBar;
