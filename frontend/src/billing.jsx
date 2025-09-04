import React, { useState } from 'react';

// The main App component for billing.
const App = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Initiates a Stripe checkout session for a given plan.
   * @param {string} plan The name of the billing plan (e.g., 'basic', 'premium').
   */
  const goCheckout = async (plan) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("/api/billing/stripe/checkout", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ plan })
      });

      if (!response.ok) {
        throw new Error('Failed to start checkout session.');
      }

      const { url } = await response.json();
      if (url) {
        // Redirect the user to the Stripe checkout page.
        window.location.href = url;
      } else {
        throw new Error('No URL returned from the checkout API.');
      }

    } catch (err) {
      console.error("Checkout error:", err);
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4 font-sans text-gray-800">
      <div className="bg-white rounded-3xl shadow-2xl p-8 max-w-xl w-full flex flex-col items-center">
        <h1 className="text-4xl font-extrabold text-center text-gray-900 mb-2">
          Choose Your Plan
        </h1>
        <p className="text-md text-gray-500 text-center mb-8">
          Unlock powerful features with a plan that fits your needs.
        </p>

        {loading && (
          <div className="flex items-center justify-center py-4">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
            <p className="ml-3 text-gray-600">Redirecting to checkout...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-xl relative mb-4 w-full text-center">
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        <div className="flex flex-col md:flex-row space-y-6 md:space-y-0 md:space-x-6 w-full">
          {/* Basic Plan */}
          <div className="bg-gray-50 p-6 rounded-2xl shadow-lg border border-gray-200 flex-1 flex flex-col transition-all duration-300 transform hover:scale-105">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Basic Plan</h2>
            <p className="text-gray-600">Essential features to get you started.</p>
            <p className="text-4xl font-bold my-4">$10<span className="text-lg font-normal text-gray-500">/month</span></p>
            <ul className="text-gray-700 space-y-2 mb-6 flex-grow">
              <li className="flex items-center">
                <span className="text-teal-500 mr-2">✓</span> Feature A
              </li>
              <li className="flex items-center">
                <span className="text-teal-500 mr-2">✓</span> Feature B
              </li>
              <li className="flex items-center">
                <span className="text-teal-500 mr-2">✓</span> Feature C
              </li>
            </ul>
            <button
              onClick={() => goCheckout('basic-plan')}
              disabled={loading}
              className="mt-auto w-full px-6 py-3 bg-gray-900 text-white font-bold rounded-full shadow-lg hover:bg-gray-700 transition-colors duration-300 disabled:opacity-50"
            >
              {loading ? 'Processing...' : 'Choose Basic'}
            </button>
          </div>

          {/* Premium Plan */}
          <div className="bg-gray-900 p-6 rounded-2xl shadow-2xl border border-gray-700 flex-1 flex flex-col transition-all duration-300 transform hover:scale-105">
            <h2 className="text-2xl font-bold text-white mb-2">Premium Plan</h2>
            <p className="text-gray-300">Advanced tools for professionals.</p>
            <p className="text-4xl font-bold text-white my-4">$25<span className="text-lg font-normal text-gray-400">/month</span></p>
            <ul className="text-gray-300 space-y-2 mb-6 flex-grow">
              <li className="flex items-center">
                <span className="text-teal-500 mr-2">✓</span> All Basic Features
              </li>
              <li className="flex items-center">
                <span className="text-teal-500 mr-2">✓</span> Advanced Analytics
              </li>
              <li className="flex items-center">
                <span className="text-teal-500 mr-2">✓</span> Priority Support
              </li>
            </ul>
            <button
              onClick={() => goCheckout('premium-plan')}
              disabled={loading}
              className="mt-auto w-full px-6 py-3 bg-teal-500 text-white font-bold rounded-full shadow-lg hover:bg-teal-400 transition-colors duration-300 disabled:opacity-50"
            >
              {loading ? 'Processing...' : 'Choose Premium'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
