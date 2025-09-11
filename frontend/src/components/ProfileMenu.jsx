// frontend/src/components/ProfileMenu.jsx
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { User, Settings, LogOut, Plus, ChevronDown, UserCheck } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTranslation } from 'react-i18next';

const ProfileMenu = ({ onAuth }) => {
  const { t } = useTranslation();
  const { user, isAuthenticated, currentProfile, profiles, signOut, switchProfile } = useAuth();
  const [isOpen, setIsOpen] = useState(false);

  const handleProfileSwitch = (profileId) => {
    switchProfile(profileId);
    setIsOpen(false);
  };

  const handleSignOut = () => {
    signOut();
    setIsOpen(false);
  };

  const getInitials = (name) => {
    return name
      .split(' ')
      .map(word => word.charAt(0))
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  const getAvatarColor = (name) => {
    const colors = [
      'bg-indigo-500',
      'bg-purple-500',
      'bg-pink-500',
      'bg-red-500',
      'bg-orange-500',
      'bg-yellow-500',
      'bg-green-500',
      'bg-teal-500',
      'bg-blue-500',
      'bg-cyan-500'
    ];
    
    const index = name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return colors[index % colors.length];
  };

  if (!isAuthenticated) {
    return (
      <button
        onClick={onAuth}
        className="flex items-center gap-2 px-3 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 transition-colors"
      >
        <User size={16} />
        <span className="text-sm font-medium">{t('auth.sign_in') || 'Sign In'}</span>
      </button>
    );
  }

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors"
      >
        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-medium ${getAvatarColor(user?.name || 'User')}`}>
          {user?.avatar ? (
            <img src={user.avatar} alt={user.name} className="w-8 h-8 rounded-full" />
          ) : (
            getInitials(user?.name || 'User')
          )}
        </div>
        
        <div className="hidden sm:block text-left">
          <p className="text-sm font-medium text-gray-900 dark:text-white">
            {user?.name || 'User'}
          </p>
          {currentProfile && (
            <p className="text-xs text-gray-500 dark:text-gray-400">
              {currentProfile.name}
            </p>
          )}
        </div>
        
        <ChevronDown size={16} className={`text-gray-500 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-10"
              onClick={() => setIsOpen(false)}
            />
            
            {/* Dropdown */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: -10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: -10 }}
              className="absolute right-0 mt-2 w-64 bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-gray-200 dark:border-slate-700 z-20"
            >
              {/* User Info */}
              <div className="p-4 border-b border-gray-200 dark:border-slate-700">
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center text-white font-medium ${getAvatarColor(user?.name || 'User')}`}>
                    {user?.avatar ? (
                      <img src={user.avatar} alt={user.name} className="w-10 h-10 rounded-full" />
                    ) : (
                      getInitials(user?.name || 'User')
                    )}
                  </div>
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">
                      {user?.name || 'User'}
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {user?.isGuest ? t('auth.guest_user') || 'Guest User' : user?.email}
                    </p>
                  </div>
                </div>
              </div>

              {/* Profiles Section */}
              {profiles.length > 0 && (
                <div className="p-2">
                  <div className="px-2 py-1 text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                    {t('profiles.profiles') || 'Profiles'}
                  </div>
                  {profiles.map((profile) => (
                    <button
                      key={profile.id}
                      onClick={() => handleProfileSwitch(profile.id)}
                      className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left transition-colors ${
                        currentProfile?.id === profile.id
                          ? 'bg-indigo-50 dark:bg-indigo-900/20 text-indigo-700 dark:text-indigo-300'
                          : 'hover:bg-gray-50 dark:hover:bg-slate-700 text-gray-700 dark:text-gray-300'
                      }`}
                    >
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-medium ${getAvatarColor(profile.name)}`}>
                        {getInitials(profile.name)}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium truncate">
                          {profile.name}
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                          {profile.location}
                        </p>
                      </div>
                      {currentProfile?.id === profile.id && (
                        <UserCheck size={16} className="text-indigo-600 dark:text-indigo-400" />
                      )}
                    </button>
                  ))}
                </div>
              )}

              {/* Actions */}
              <div className="p-2 border-t border-gray-200 dark:border-slate-700">
                <button
                  onClick={() => {
                    setIsOpen(false);
                    // TODO: Open add profile modal
                  }}
                  className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left hover:bg-gray-50 dark:hover:bg-slate-700 text-gray-700 dark:text-gray-300 transition-colors"
                >
                  <div className="w-8 h-8 rounded-full bg-gray-100 dark:bg-slate-700 flex items-center justify-center">
                    <Plus size={16} className="text-gray-600 dark:text-gray-400" />
                  </div>
                  <span className="text-sm font-medium">
                    {t('profiles.add_profile') || 'Add Profile'}
                  </span>
                </button>

                <button
                  onClick={() => {
                    setIsOpen(false);
                    // TODO: Open settings modal
                  }}
                  className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left hover:bg-gray-50 dark:hover:bg-slate-700 text-gray-700 dark:text-gray-300 transition-colors"
                >
                  <div className="w-8 h-8 rounded-full bg-gray-100 dark:bg-slate-700 flex items-center justify-center">
                    <Settings size={16} className="text-gray-600 dark:text-gray-400" />
                  </div>
                  <span className="text-sm font-medium">
                    {t('common.settings') || 'Settings'}
                  </span>
                </button>

                <button
                  onClick={handleSignOut}
                  className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left hover:bg-red-50 dark:hover:bg-red-900/20 text-red-600 dark:text-red-400 transition-colors"
                >
                  <div className="w-8 h-8 rounded-full bg-red-100 dark:bg-red-900/20 flex items-center justify-center">
                    <LogOut size={16} className="text-red-600 dark:text-red-400" />
                  </div>
                  <span className="text-sm font-medium">
                    {t('auth.sign_out') || 'Sign Out'}
                  </span>
                </button>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
};

export default ProfileMenu;
