// frontend/src/components/QuickActions.jsx
import { motion } from 'framer-motion';
import { Bell, Calendar, Clock, Plus, Sparkles, User } from 'lucide-react';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';

const QuickActions = ({ onQuick }) => {
  const { t } = useTranslation();
  const { isAuthenticated, currentProfile } = useAuth();

  // Debug logging
  console.log("QuickActions props:", { onQuick });
  console.log("QuickActions auth state:", { isAuthenticated, currentProfile });
  console.log("QuickActions onQuick function type:", typeof onQuick);

  const quickActions = [
    {
      id: 'panchangam',
      label: t('panchangam.title'),
      icon: Calendar,
      query: "Show today's Panchangam",
      color: 'from-yellow-500 to-orange-500',
      description: t('panchangam.today_panchangam')
    },
    {
      id: 'chart',
      label: t('birth_chart.title'),
      icon: User,
      query: "Show my birth chart",
      color: 'from-blue-500 to-purple-500',
      description: t('birth_chart.birth_chart')
    },
    {
      id: 'dasha',
      label: t('dasha.title'),
      icon: Clock,
      query: "Show my Dasha periods",
      color: 'from-green-500 to-teal-500',
      description: t('dasha.dasha_timeline')
    },
    {
      id: 'reminders',
      label: t('reminders.title'),
      icon: Bell,
      query: "Show my reminders and events",
      color: 'from-pink-500 to-rose-500',
      description: t('reminders.reminders_events')
    },
    {
      id: 'profile',
      label: t('profiles.create_profile'),
      icon: Plus,
      query: "Add a new profile",
      color: 'from-indigo-500 to-blue-500',
      description: t('profiles.create_new_profile')
    },
    {
      id: 'reading',
      label: t('reading.title'),
      icon: Sparkles,
      query: "Generate my personal reading",
      color: 'from-purple-500 to-pink-500',
      description: t('reading.generate_reading')
    }
  ];

  const handleQuickAction = (action) => {
    console.log("handleQuickAction called with:", action);
    console.log("onQuick function:", onQuick);

    if (!isAuthenticated) {
      console.log("User not authenticated, showing sign in message");
      onQuick("Please sign in first to access this feature");
      return;
    }

    if (action.id === 'chart' && !currentProfile) {
      console.log("No profile for chart action");
      onQuick("Please add a profile first to view your birth chart");
      return;
    }

    if (action.id === 'dasha' && !currentProfile) {
      console.log("No profile for dasha action");
      onQuick("Please add a profile first to view your Dasha periods");
      return;
    }

    console.log("Calling onQuick with query:", action.query);
    onQuick(action.query);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-6"
    >
      <div className="text-center mb-4">
        <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">
          {t('common.quick_actions') || 'Quick Actions'}
        </h3>
        <p className="text-xs text-gray-500 dark:text-gray-500">
          {t('common.click_to_explore') || 'Click to explore Vedic astrology features'}
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {quickActions.map((action, index) => {
          const Icon = action.icon;
          const isDisabled = !isAuthenticated ||
            (['chart', 'dasha'].includes(action.id) && !currentProfile);

          return (
            <motion.button
              key={action.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => handleQuickAction(action)}
              disabled={isDisabled}
              className={`group relative p-4 rounded-xl border-2 border-transparent transition-all duration-200 ${isDisabled
                  ? 'bg-gray-100 dark:bg-gray-800 cursor-not-allowed opacity-50'
                  : 'bg-white dark:bg-slate-800 hover:border-indigo-200 dark:hover:border-indigo-800 hover:shadow-lg cursor-pointer'
                }`}
            >
              <div className="flex flex-col items-center text-center">
                <div className={`w-12 h-12 rounded-full bg-gradient-to-r ${action.color} flex items-center justify-center mb-3 ${isDisabled ? 'opacity-50' : 'group-hover:scale-110 transition-transform duration-200'
                  }`}>
                  <Icon size={20} className="text-white" />
                </div>

                <h4 className={`font-medium text-sm mb-1 ${isDisabled
                    ? 'text-gray-400 dark:text-gray-600'
                    : 'text-gray-900 dark:text-white group-hover:text-indigo-600 dark:group-hover:text-indigo-400'
                  }`}>
                  {action.label}
                </h4>

                <p className={`text-xs leading-tight ${isDisabled
                    ? 'text-gray-400 dark:text-gray-600'
                    : 'text-gray-600 dark:text-gray-400'
                  }`}>
                  {action.description}
                </p>
              </div>

              {isDisabled && (
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="bg-gray-200 dark:bg-gray-700 rounded-full p-1">
                    <svg className="w-4 h-4 text-gray-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                </div>
              )}
            </motion.button>
          );
        })}
      </div>

      {!isAuthenticated && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-4 p-3 bg-indigo-50 dark:bg-indigo-900/20 rounded-lg border border-indigo-200 dark:border-indigo-800"
        >
          <p className="text-sm text-indigo-700 dark:text-indigo-300 text-center">
            {t('common.sign_in_to_access') || 'Sign in to access all features and save your data'}
          </p>
        </motion.div>
      )}

      {isAuthenticated && !currentProfile && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-4 p-3 bg-amber-50 dark:bg-amber-900/20 rounded-lg border border-amber-200 dark:border-amber-800"
        >
          <p className="text-sm text-amber-700 dark:text-amber-300 text-center">
            {t('common.add_profile_first') || 'Add a profile to access birth chart and Dasha features'}
          </p>
        </motion.div>
      )}
    </motion.div>
  );
};

export default QuickActions;
