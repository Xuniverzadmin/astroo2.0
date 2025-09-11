// frontend/src/components/ProfilesDashboard.jsx
import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import ProfileForm from './ProfileForm';

const ProfilesDashboard = () => {
  const { t } = useTranslation();
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingProfile, setEditingProfile] = useState(null);
  const [selectedProfile, setSelectedProfile] = useState(null);

  useEffect(() => {
    fetchProfiles();
  }, []);

  const fetchProfiles = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/profiles');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setProfiles(data.profiles || []);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching profiles:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProfile = () => {
    setEditingProfile(null);
    setShowForm(true);
  };

  const handleEditProfile = (profile) => {
    setEditingProfile(profile);
    setShowForm(true);
  };

  const handleSaveProfile = async (profileData) => {
    try {
      const url = editingProfile ? `/api/profiles/${editingProfile.id}` : '/api/profiles';
      const method = editingProfile ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(profileData),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      await fetchProfiles(); // Refresh the list
      setShowForm(false);
      setEditingProfile(null);
    } catch (error) {
      console.error('Error saving profile:', error);
      throw error;
    }
  };

  const handleDeleteProfile = async (profileId) => {
    if (!window.confirm(t('confirm_delete_profile'))) {
      return;
    }
    
    try {
      const response = await fetch(`/api/profiles/${profileId}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      await fetchProfiles(); // Refresh the list
    } catch (error) {
      console.error('Error deleting profile:', error);
      setError(error.message);
    }
  };

  const handleSelectProfile = (profile) => {
    setSelectedProfile(profile);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const calculateAge = (birthDate) => {
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    
    return age;
  };

  if (loading) {
    return (
      <div className="profiles-dashboard bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">{t('loading_profiles')}</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="profiles-dashboard bg-white rounded-lg shadow-md p-6">
        <div className="text-red-600 text-center">
          <p>{t('error_loading_profiles')}</p>
          <p className="text-sm text-gray-500">{error}</p>
          <button 
            onClick={fetchProfiles}
            className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            {t('retry')}
          </button>
        </div>
      </div>
    );
  }

  if (showForm) {
    return (
      <ProfileForm
        profile={editingProfile}
        onSave={handleSaveProfile}
        onCancel={() => {
          setShowForm(false);
          setEditingProfile(null);
        }}
        isEditing={!!editingProfile}
      />
    );
  }

  return (
    <div className="profiles-dashboard bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">{t('profiles')}</h2>
        <button
          onClick={handleCreateProfile}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          {t('create_new_profile')}
        </button>
      </div>

      {profiles.length === 0 ? (
        <div className="text-center py-8">
          <div className="text-gray-500 mb-4">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">{t('no_profiles_yet')}</h3>
          <p className="text-gray-500 mb-4">{t('create_your_first_profile')}</p>
          <button
            onClick={handleCreateProfile}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            {t('create_profile')}
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {profiles.map((profile) => (
            <div
              key={profile.id}
              className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                selectedProfile?.id === profile.id
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => handleSelectProfile(profile)}
            >
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="font-semibold text-gray-800">{profile.name}</h3>
                  <p className="text-sm text-gray-600">
                    {t('age')}: {calculateAge(profile.birth_date)} {t('years')}
                  </p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleEditProfile(profile);
                    }}
                    className="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    {t('edit')}
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteProfile(profile.id);
                    }}
                    className="text-red-600 hover:text-red-800 text-sm"
                  >
                    {t('delete')}
                  </button>
                </div>
              </div>

              <div className="space-y-2 text-sm text-gray-600">
                <div>
                  <span className="font-medium">{t('birth_date')}:</span> {formatDate(profile.birth_date)}
                </div>
                <div>
                  <span className="font-medium">{t('birth_time')}:</span> {profile.birth_time}
                </div>
                <div>
                  <span className="font-medium">{t('birth_place')}:</span> {profile.birth_place}
                </div>
                <div>
                  <span className="font-medium">{t('timezone')}:</span> {profile.timezone}
                </div>
              </div>

              {profile.notes && (
                <div className="mt-3 pt-3 border-t border-gray-200">
                  <p className="text-sm text-gray-600">
                    <span className="font-medium">{t('notes')}:</span> {profile.notes}
                  </p>
                </div>
              )}

              <div className="mt-3 pt-3 border-t border-gray-200">
                <div className="flex gap-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      // TODO: Navigate to birth chart
                      console.log('View birth chart for:', profile.id);
                    }}
                    className="flex-1 px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700"
                  >
                    {t('view_chart')}
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      // TODO: Navigate to dasha
                      console.log('View dasha for:', profile.id);
                    }}
                    className="flex-1 px-3 py-1 bg-purple-600 text-white text-sm rounded hover:bg-purple-700"
                  >
                    {t('view_dasha')}
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {selectedProfile && (
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="font-semibold text-gray-800 mb-2">{t('selected_profile')}</h3>
          <p className="text-sm text-gray-600">
            {t('selected_profile_info', { name: selectedProfile.name, age: calculateAge(selectedProfile.birth_date) })}
          </p>
        </div>
      )}
    </div>
  );
};

export default ProfilesDashboard;
