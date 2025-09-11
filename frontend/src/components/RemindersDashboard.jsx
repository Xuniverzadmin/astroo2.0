// frontend/src/components/RemindersDashboard.jsx
import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

const RemindersDashboard = ({ userId }) => {
  const { t } = useTranslation();
  const [reminders, setReminders] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);

  useEffect(() => {
    fetchData();
  }, [userId]);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Fetch reminders and events in parallel
      const [remindersResponse, eventsResponse] = await Promise.all([
        fetch(`/api/reminders/${userId || 'current'}`),
        fetch('/api/events/upcoming?days_ahead=30')
      ]);
      
      if (!remindersResponse.ok) {
        throw new Error(`HTTP error! status: ${remindersResponse.status}`);
      }
      
      if (!eventsResponse.ok) {
        throw new Error(`HTTP error! status: ${eventsResponse.status}`);
      }
      
      const remindersData = await remindersResponse.json();
      const eventsData = await eventsResponse.json();
      
      setReminders(remindersData.reminders || []);
      setEvents(eventsData.events || []);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateReminder = async (reminderData) => {
    try {
      const response = await fetch('/api/reminders/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(reminderData),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      await fetchData(); // Refresh the list
      setShowCreateForm(false);
    } catch (error) {
      console.error('Error creating reminder:', error);
      throw error;
    }
  };

  const handleDeleteReminder = async (reminderId) => {
    if (!window.confirm(t('confirm_delete_reminder'))) {
      return;
    }
    
    try {
      const response = await fetch(`/api/reminders/${reminderId}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      await fetchData(); // Refresh the list
    } catch (error) {
      console.error('Error deleting reminder:', error);
      setError(error.message);
    }
  };

  const handleMarkSent = async (reminderId) => {
    try {
      const response = await fetch(`/api/reminders/${reminderId}/mark-sent`, {
        method: 'PUT',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      await fetchData(); // Refresh the list
    } catch (error) {
      console.error('Error marking reminder as sent:', error);
      setError(error.message);
    }
  };

  const formatDateTime = (dateTimeString) => {
    return new Date(dateTimeString).toLocaleString();
  };

  const getEventTypeColor = (eventType) => {
    const colors = {
      'auspicious': 'bg-green-100 text-green-800 border-green-200',
      'inauspicious': 'bg-red-100 text-red-800 border-red-200',
      'neutral': 'bg-gray-100 text-gray-800 border-gray-200'
    };
    return colors[eventType] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getReminderStatusColor = (isSent) => {
    return isSent ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800';
  };

  if (loading) {
    return (
      <div className="reminders-dashboard bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">{t('loading_reminders')}</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="reminders-dashboard bg-white rounded-lg shadow-md p-6">
        <div className="text-red-600 text-center">
          <p>{t('error_loading_reminders')}</p>
          <p className="text-sm text-gray-500">{error}</p>
          <button 
            onClick={fetchData}
            className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            {t('retry')}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="reminders-dashboard bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">{t('reminders_events')}</h2>
        <button
          onClick={() => setShowCreateForm(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          {t('create_reminder')}
        </button>
      </div>

      {/* Create Reminder Form */}
      {showCreateForm && (
        <div className="bg-gray-50 p-4 rounded-lg mb-6">
          <h3 className="font-semibold text-gray-800 mb-3">{t('create_new_reminder')}</h3>
          <CreateReminderForm
            events={events}
            onSubmit={handleCreateReminder}
            onCancel={() => setShowCreateForm(false)}
          />
        </div>
      )}

      {/* Upcoming Events */}
      <div className="mb-8">
        <h3 className="font-semibold text-gray-800 mb-4">{t('upcoming_events')}</h3>
        {events.length === 0 ? (
          <div className="text-center py-4 text-gray-500">
            <p>{t('no_upcoming_events')}</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {events.map((event) => (
              <div
                key={event.event_id}
                className={`border rounded-lg p-4 cursor-pointer transition-colors ${
                  selectedEvent?.event_id === event.event_id
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => setSelectedEvent(event)}
              >
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-medium text-gray-800">{event.name}</h4>
                  <span className={`px-2 py-1 rounded-full text-xs border ${getEventTypeColor(event.event_type)}`}>
                    {t(event.event_type)}
                  </span>
                </div>
                
                <div className="space-y-1 text-sm text-gray-600">
                  <div>
                    <span className="font-medium">{t('date')}:</span> {new Date(event.event_date).toLocaleDateString()}
                  </div>
                  {event.event_time && (
                    <div>
                      <span className="font-medium">{t('time')}:</span> {event.event_time}
                    </div>
                  )}
                  <div>
                    <span className="font-medium">{t('significance')}:</span> {event.significance}
                  </div>
                </div>

                {event.recommendations && event.recommendations.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <p className="text-xs font-medium text-gray-600 mb-1">{t('recommendations')}:</p>
                    <ul className="text-xs text-gray-600 space-y-1">
                      {event.recommendations.slice(0, 2).map((rec, index) => (
                        <li key={index}>• {rec}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Reminders */}
      <div className="mb-6">
        <h3 className="font-semibold text-gray-800 mb-4">{t('your_reminders')}</h3>
        {reminders.length === 0 ? (
          <div className="text-center py-4 text-gray-500">
            <p>{t('no_reminders_yet')}</p>
            <button
              onClick={() => setShowCreateForm(true)}
              className="mt-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              {t('create_first_reminder')}
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            {reminders.map((reminder) => (
              <div
                key={reminder.reminder_id}
                className="border border-gray-200 rounded-lg p-4"
              >
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h4 className="font-medium text-gray-800">{reminder.message}</h4>
                    <p className="text-sm text-gray-600">
                      {t('reminder_time')}: {formatDateTime(reminder.reminder_time)}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-1 rounded-full text-xs ${getReminderStatusColor(reminder.is_sent)}`}>
                      {reminder.is_sent ? t('sent') : t('pending')}
                    </span>
                    <div className="flex gap-1">
                      {!reminder.is_sent && (
                        <button
                          onClick={() => handleMarkSent(reminder.reminder_id)}
                          className="text-green-600 hover:text-green-800 text-sm"
                        >
                          {t('mark_sent')}
                        </button>
                      )}
                      <button
                        onClick={() => handleDeleteReminder(reminder.reminder_id)}
                        className="text-red-600 hover:text-red-800 text-sm"
                      >
                        {t('delete')}
                      </button>
                    </div>
                  </div>
                </div>
                
                <div className="text-sm text-gray-600">
                  <span className="font-medium">{t('notification_type')}:</span> {t(reminder.notification_type)}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Selected Event Details */}
      {selectedEvent && (
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="font-semibold text-gray-800 mb-3">{t('event_details')}</h3>
          <div className="space-y-2 text-sm">
            <div>
              <span className="font-medium text-gray-600">{t('name')}:</span>
              <p className="text-gray-800">{selectedEvent.name}</p>
            </div>
            <div>
              <span className="font-medium text-gray-600">{t('description')}:</span>
              <p className="text-gray-800">{selectedEvent.description}</p>
            </div>
            <div>
              <span className="font-medium text-gray-600">{t('significance')}:</span>
              <p className="text-gray-800">{selectedEvent.significance}</p>
            </div>
            {selectedEvent.recommendations && selectedEvent.recommendations.length > 0 && (
              <div>
                <span className="font-medium text-gray-600">{t('recommendations')}:</span>
                <ul className="text-gray-800 list-disc list-inside">
                  {selectedEvent.recommendations.map((rec, index) => (
                    <li key={index}>{rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

// Create Reminder Form Component
const CreateReminderForm = ({ events, onSubmit, onCancel }) => {
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    event_id: '',
    message: '',
    reminder_time: '',
    notification_type: 'email'
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

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
    
    // Basic validation
    const newErrors = {};
    if (!formData.event_id) newErrors.event_id = t('event_required');
    if (!formData.message.trim()) newErrors.message = t('message_required');
    if (!formData.reminder_time) newErrors.reminder_time = t('reminder_time_required');
    
    setErrors(newErrors);
    if (Object.keys(newErrors).length > 0) return;
    
    setLoading(true);
    
    try {
      await onSubmit({
        ...formData,
        user_id: 'current', // TODO: Get actual user ID
        is_sent: false
      });
    } catch (error) {
      setErrors({ submit: t('error_creating_reminder') });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="event_id" className="block text-sm font-medium text-gray-700 mb-2">
          {t('select_event')} *
        </label>
        <select
          id="event_id"
          name="event_id"
          value={formData.event_id}
          onChange={handleInputChange}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.event_id ? 'border-red-500' : 'border-gray-300'
          }`}
        >
          <option value="">{t('choose_event')}</option>
          {events.map((event) => (
            <option key={event.event_id} value={event.event_id}>
              {event.name} - {new Date(event.event_date).toLocaleDateString()}
            </option>
          ))}
        </select>
        {errors.event_id && <p className="mt-1 text-sm text-red-600">{errors.event_id}</p>}
      </div>

      <div>
        <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
          {t('reminder_message')} *
        </label>
        <textarea
          id="message"
          name="message"
          value={formData.message}
          onChange={handleInputChange}
          rows={3}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.message ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder={t('enter_reminder_message')}
        />
        {errors.message && <p className="mt-1 text-sm text-red-600">{errors.message}</p>}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label htmlFor="reminder_time" className="block text-sm font-medium text-gray-700 mb-2">
            {t('reminder_time')} *
          </label>
          <input
            type="datetime-local"
            id="reminder_time"
            name="reminder_time"
            value={formData.reminder_time}
            onChange={handleInputChange}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              errors.reminder_time ? 'border-red-500' : 'border-gray-300'
            }`}
          />
          {errors.reminder_time && <p className="mt-1 text-sm text-red-600">{errors.reminder_time}</p>}
        </div>

        <div>
          <label htmlFor="notification_type" className="block text-sm font-medium text-gray-700 mb-2">
            {t('notification_type')}
          </label>
          <select
            id="notification_type"
            name="notification_type"
            value={formData.notification_type}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="email">{t('email')}</option>
            <option value="sms">{t('sms')}</option>
            <option value="push">{t('push_notification')}</option>
          </select>
        </div>
      </div>

      {errors.submit && (
        <div className="text-red-600 text-sm">{errors.submit}</div>
      )}

      <div className="flex justify-end gap-4">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
        >
          {t('cancel')}
        </button>
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? t('creating') : t('create_reminder')}
        </button>
      </div>
    </form>
  );
};

export default RemindersDashboard;
