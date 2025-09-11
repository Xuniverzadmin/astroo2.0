// frontend/src/components/ProfileForm.jsx
import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

const ProfileForm = ({ profile, onSave, onCancel, isEditing = false }) => {
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    name: '',
    birthDate: '',
    birthTime: '',
    birthPlace: '',
    latitude: '',
    longitude: '',
    timezone: 'Asia/Kolkata',
    gender: '',
    notes: ''
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (profile && isEditing) {
      setFormData({
        name: profile.name || '',
        birthDate: profile.birth_date || '',
        birthTime: profile.birth_time || '',
        birthPlace: profile.birth_place || '',
        latitude: profile.latitude || '',
        longitude: profile.longitude || '',
        timezone: profile.timezone || 'Asia/Kolkata',
        gender: profile.gender || '',
        notes: profile.notes || ''
      });
    }
  }, [profile, isEditing]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.name.trim()) {
      newErrors.name = t('name_required');
    }
    
    if (!formData.birthDate) {
      newErrors.birthDate = t('birth_date_required');
    }
    
    if (!formData.birthTime) {
      newErrors.birthTime = t('birth_time_required');
    }
    
    if (!formData.birthPlace.trim()) {
      newErrors.birthPlace = t('birth_place_required');
    }
    
    if (!formData.latitude || isNaN(parseFloat(formData.latitude))) {
      newErrors.latitude = t('valid_latitude_required');
    }
    
    if (!formData.longitude || isNaN(parseFloat(formData.longitude))) {
      newErrors.longitude = t('valid_longitude_required');
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setLoading(true);
    
    try {
      const profileData = {
        ...formData,
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude)
      };
      
      await onSave(profileData);
    } catch (error) {
      console.error('Error saving profile:', error);
      setErrors({ submit: t('error_saving_profile') });
    } finally {
      setLoading(false);
    }
  };

  const handleLocationSearch = async () => {
    if (!formData.birthPlace.trim()) return;
    
    try {
      // TODO: Implement geocoding API call
      console.log('Searching for location:', formData.birthPlace);
    } catch (error) {
      console.error('Error searching location:', error);
    }
  };

  return (
    <div className="profile-form bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">
          {isEditing ? t('edit_profile') : t('create_profile')}
        </h2>
        {onCancel && (
          <button
            onClick={onCancel}
            className="text-gray-500 hover:text-gray-700"
          >
            {t('cancel')}
          </button>
        )}
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
              {t('full_name')} *
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.name ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder={t('enter_full_name')}
            />
            {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name}</p>}
          </div>

          <div>
            <label htmlFor="gender" className="block text-sm font-medium text-gray-700 mb-2">
              {t('gender')}
            </label>
            <select
              id="gender"
              name="gender"
              value={formData.gender}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">{t('select_gender')}</option>
              <option value="male">{t('male')}</option>
              <option value="female">{t('female')}</option>
              <option value="other">{t('other')}</option>
            </select>
          </div>
        </div>

        {/* Birth Information */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="birthDate" className="block text-sm font-medium text-gray-700 mb-2">
              {t('birth_date')} *
            </label>
            <input
              type="date"
              id="birthDate"
              name="birthDate"
              value={formData.birthDate}
              onChange={handleInputChange}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.birthDate ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {errors.birthDate && <p className="mt-1 text-sm text-red-600">{errors.birthDate}</p>}
          </div>

          <div>
            <label htmlFor="birthTime" className="block text-sm font-medium text-gray-700 mb-2">
              {t('birth_time')} *
            </label>
            <input
              type="time"
              id="birthTime"
              name="birthTime"
              value={formData.birthTime}
              onChange={handleInputChange}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.birthTime ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {errors.birthTime && <p className="mt-1 text-sm text-red-600">{errors.birthTime}</p>}
          </div>
        </div>

        {/* Location Information */}
        <div>
          <label htmlFor="birthPlace" className="block text-sm font-medium text-gray-700 mb-2">
            {t('birth_place')} *
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              id="birthPlace"
              name="birthPlace"
              value={formData.birthPlace}
              onChange={handleInputChange}
              className={`flex-1 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.birthPlace ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder={t('enter_birth_place')}
            />
            <button
              type="button"
              onClick={handleLocationSearch}
              className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
            >
              {t('search')}
            </button>
          </div>
          {errors.birthPlace && <p className="mt-1 text-sm text-red-600">{errors.birthPlace}</p>}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label htmlFor="latitude" className="block text-sm font-medium text-gray-700 mb-2">
              {t('latitude')} *
            </label>
            <input
              type="number"
              id="latitude"
              name="latitude"
              value={formData.latitude}
              onChange={handleInputChange}
              step="0.000001"
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.latitude ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="12.9716"
            />
            {errors.latitude && <p className="mt-1 text-sm text-red-600">{errors.latitude}</p>}
          </div>

          <div>
            <label htmlFor="longitude" className="block text-sm font-medium text-gray-700 mb-2">
              {t('longitude')} *
            </label>
            <input
              type="number"
              id="longitude"
              name="longitude"
              value={formData.longitude}
              onChange={handleInputChange}
              step="0.000001"
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                errors.longitude ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="77.5946"
            />
            {errors.longitude && <p className="mt-1 text-sm text-red-600">{errors.longitude}</p>}
          </div>

          <div>
            <label htmlFor="timezone" className="block text-sm font-medium text-gray-700 mb-2">
              {t('timezone')} *
            </label>
            <select
              id="timezone"
              name="timezone"
              value={formData.timezone}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="Asia/Kolkata">Asia/Kolkata (IST)</option>
              <option value="Asia/Dubai">Asia/Dubai (GST)</option>
              <option value="America/New_York">America/New_York (EST)</option>
              <option value="Europe/London">Europe/London (GMT)</option>
              <option value="Asia/Singapore">Asia/Singapore (SGT)</option>
            </select>
          </div>
        </div>

        {/* Notes */}
        <div>
          <label htmlFor="notes" className="block text-sm font-medium text-gray-700 mb-2">
            {t('notes')}
          </label>
          <textarea
            id="notes"
            name="notes"
            value={formData.notes}
            onChange={handleInputChange}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder={t('additional_notes')}
          />
        </div>

        {/* Submit Error */}
        {errors.submit && (
          <div className="text-red-600 text-sm">{errors.submit}</div>
        )}

        {/* Submit Button */}
        <div className="flex justify-end gap-4">
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className="px-6 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
            >
              {t('cancel')}
            </button>
          )}
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? t('saving') : (isEditing ? t('update_profile') : t('create_profile'))}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ProfileForm;
