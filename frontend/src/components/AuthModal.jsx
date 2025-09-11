// frontend/src/components/AuthModal.jsx
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, User, Mail, Calendar, MapPin, Clock, Eye, EyeOff, Loader } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useProfile } from '../hooks/useProfile';
import { useTranslation } from 'react-i18next';
import toast from 'react-hot-toast';

const AuthModal = ({ onClose }) => {
  const { t } = useTranslation();
  const { signIn, continueAsGuest } = useAuth();
  const { getCurrentLocation, validateProfile } = useProfile();
  
  const [isSignUp, setIsSignUp] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState({});
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    birthDate: '',
    birthTime: '',
    location: '',
    latitude: '',
    longitude: '',
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || 'Asia/Kolkata'
  });

  // Auto-fill location on mount
  useEffect(() => {
    const autoFillLocation = async () => {
      try {
        const location = await getCurrentLocation();
        setFormData(prev => ({
          ...prev,
          latitude: location.latitude.toString(),
          longitude: location.longitude.toString()
        }));
        
        // Try to get city name from coordinates (simplified)
        setFormData(prev => ({
          ...prev,
          location: 'Your Location' // TODO: Implement reverse geocoding
        }));
      } catch (error) {
        console.log('Could not get location:', error);
        // Use default location
        setFormData(prev => ({
          ...prev,
          latitude: '13.0827',
          longitude: '80.2707',
          location: 'Chennai, India'
        }));
      }
    };
    
    autoFillLocation();
  }, [getCurrentLocation]);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setErrors({});

    try {
      // Validate form
      const validation = validateProfile(formData);
      if (!validation.isValid) {
        setErrors(validation.errors);
        setIsLoading(false);
        return;
      }

      // Additional validation for auth fields
      if (isSignUp && !formData.email) {
        setErrors(prev => ({ ...prev, email: 'Email is required for sign up' }));
        setIsLoading(false);
        return;
      }

      if (isSignUp && !formData.password) {
        setErrors(prev => ({ ...prev, password: 'Password is required for sign up' }));
        setIsLoading(false);
        return;
      }

      // Sign in/up
      const result = await signIn({
        name: formData.name,
        email: formData.email || null,
        password: formData.password || null,
        birthDate: formData.birthDate,
        birthTime: formData.birthTime,
        location: formData.location,
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude),
        timezone: formData.timezone
      });

      if (result.success) {
        toast.success(isSignUp ? 'Account created successfully!' : 'Welcome back!');
        onClose();
      } else {
        toast.error(result.error || 'Something went wrong');
      }
    } catch (error) {
      console.error('Auth error:', error);
      toast.error('Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGuestContinue = async () => {
    setIsLoading(true);
    try {
      const result = continueAsGuest();
      if (result.success) {
        toast.success('Welcome! You can sign up later to save your data.');
        onClose();
      }
    } catch (error) {
      console.error('Guest continue error:', error);
      toast.error('Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.9, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.9, y: 20 }}
          className="bg-white dark:bg-slate-900 rounded-2xl shadow-2xl w-full max-w-md max-h-[90vh] overflow-y-auto"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-slate-700">
            <div>
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                {isSignUp ? t('auth.welcome') || 'Welcome to Astrooverz' : t('auth.sign_in') || 'Sign In'}
              </h2>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {isSignUp ? t('auth.create_account') || 'Create your account to get started' : t('auth.welcome_back') || 'Welcome back!'}
              </p>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-lg transition-colors"
            >
              <X size={20} className="text-gray-500" />
            </button>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="p-6 space-y-4">
            {/* Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <User size={16} className="inline mr-2" />
                {t('profiles.full_name')} *
              </label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                  errors.name ? 'border-red-500' : 'border-gray-300 dark:border-slate-600'
                } bg-white dark:bg-slate-800 text-gray-900 dark:text-white`}
                placeholder={t('profiles.enter_full_name') || 'Enter your full name'}
                required
              />
              {errors.name && <p className="mt-1 text-sm text-red-600">{errors.name}</p>}
            </div>

            {/* Email (only for sign up) */}
            {isSignUp && (
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  <Mail size={16} className="inline mr-2" />
                  {t('auth.email') || 'Email'} *
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                    errors.email ? 'border-red-500' : 'border-gray-300 dark:border-slate-600'
                  } bg-white dark:bg-slate-800 text-gray-900 dark:text-white`}
                  placeholder="your@email.com"
                />
                {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email}</p>}
              </div>
            )}

            {/* Password (only for sign up) */}
            {isSignUp && (
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  <Eye size={16} className="inline mr-2" />
                  {t('auth.password') || 'Password'} *
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    name="password"
                    value={formData.password}
                    onChange={handleInputChange}
                    className={`w-full px-3 py-2 pr-10 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                      errors.password ? 'border-red-500' : 'border-gray-300 dark:border-slate-600'
                    } bg-white dark:bg-slate-800 text-gray-900 dark:text-white`}
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
                {errors.password && <p className="mt-1 text-sm text-red-600">{errors.password}</p>}
              </div>
            )}

            {/* Birth Date */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <Calendar size={16} className="inline mr-2" />
                {t('profiles.birth_date')} *
              </label>
              <input
                type="date"
                name="birthDate"
                value={formData.birthDate}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                  errors.birthDate ? 'border-red-500' : 'border-gray-300 dark:border-slate-600'
                } bg-white dark:bg-slate-800 text-gray-900 dark:text-white`}
                required
              />
              {errors.birthDate && <p className="mt-1 text-sm text-red-600">{errors.birthDate}</p>}
            </div>

            {/* Birth Time */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <Clock size={16} className="inline mr-2" />
                {t('profiles.birth_time')} *
              </label>
              <input
                type="time"
                name="birthTime"
                value={formData.birthTime}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                  errors.birthTime ? 'border-red-500' : 'border-gray-300 dark:border-slate-600'
                } bg-white dark:bg-slate-800 text-gray-900 dark:text-white`}
                required
              />
              {errors.birthTime && <p className="mt-1 text-sm text-red-600">{errors.birthTime}</p>}
            </div>

            {/* Location */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                <MapPin size={16} className="inline mr-2" />
                {t('profiles.birth_place')} *
              </label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
                  errors.location ? 'border-red-500' : 'border-gray-300 dark:border-slate-600'
                } bg-white dark:bg-slate-800 text-gray-900 dark:text-white`}
                placeholder={t('profiles.enter_birth_place') || 'Enter your birth place'}
                required
              />
              {errors.location && <p className="mt-1 text-sm text-red-600">{errors.location}</p>}
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
            >
              {isLoading ? (
                <>
                  <Loader size={16} className="animate-spin" />
                  {isSignUp ? t('auth.creating') || 'Creating Account...' : t('auth.signing_in') || 'Signing In...'}
                </>
              ) : (
                isSignUp ? t('auth.create_account') || 'Create Account' : t('auth.sign_in') || 'Sign In'
              )}
            </button>

            {/* Toggle Sign In/Up */}
            <div className="text-center">
              <button
                type="button"
                onClick={() => setIsSignUp(!isSignUp)}
                className="text-sm text-indigo-600 hover:text-indigo-700 dark:text-indigo-400 dark:hover:text-indigo-300"
              >
                {isSignUp 
                  ? t('auth.already_have_account') || 'Already have an account? Sign in'
                  : t('auth.need_account') || 'Need an account? Sign up'
                }
              </button>
            </div>

            {/* Guest Continue */}
            <div className="border-t border-gray-200 dark:border-slate-700 pt-4">
              <button
                type="button"
                onClick={handleGuestContinue}
                disabled={isLoading}
                className="w-full text-gray-600 dark:text-gray-400 py-2 rounded-lg hover:bg-gray-50 dark:hover:bg-slate-800 transition-colors"
              >
                {t('auth.continue_as_guest') || 'Continue as Guest'}
              </button>
            </div>
          </form>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default AuthModal;
