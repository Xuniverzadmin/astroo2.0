import React, { useState } from 'react';

const Auth = () => {
  const [email, setEmail] = useState('');
  const [otp, setOtp] = useState('');
  const [step, setStep] = useState('request'); // 'request' or 'verify'

  const handleRequestOtp = async (e) => {
    e.preventDefault();
    try {
      await fetch('/api/auth/request-otp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });
      // If the request is successful, move to the next step
      setStep('verify');
    } catch (error) {
      console.error('Error requesting OTP:', error);
    }
  };

  const handleVerifyOtp = async (e) => {
    e.preventDefault();
    try {
      await fetch('/api/auth/verify-otp', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, code: otp }),
      });
      // If verification is successful, handle user login (e.g., redirect or update state)
      console.log('OTP verified successfully!');
    } catch (error) {
      console.error('Error verifying OTP:', error);
    }
  };

  return (
    <div>
      {step === 'request' ? (
        <form onSubmit={handleRequestOtp}>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Enter your email" required />
          <button type="submit">Request OTP</button>
        </form>
      ) : (
        <form onSubmit={handleVerifyOtp}>
          <p>An OTP has been sent to {email}.</p>
          <input type="text" value={otp} onChange={(e) => setOtp(e.target.value)} placeholder="Enter OTP" required />
          <button type="submit">Verify OTP</button>
        </form>
      )}
    </div>
  );
};

export default Auth;