import { useState } from 'react';
import { confirmSignUp } from 'aws-amplify/auth';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button } from '@/components/common/Button';
import { Input } from '@/components/common/Input';
import { handleApiError } from '@/utils/errorHandling';

interface LocationState {
  email: string;
}

/**
 * Email verification page component
 *
 * Allows users to verify their email address after signup
 */
export function Verify() {
  const [code, setCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const state = location.state as LocationState;
  const email = state?.email;

  const handleVerify = async () => {
    if (!email || !code.trim()) {
      return;
    }

    setIsLoading(true);
    try {
      // Real AWS Cognito verification
      await confirmSignUp({
        username: email,
        confirmationCode: code,
      });
      navigate('/login');
    } catch (error) {
      handleApiError(error);
    } finally {
      setIsLoading(false);
    }
  };

  if (!email) {
    navigate('/signup');
    return null;
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 animated-bg">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <div className="inline-block mb-4">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-violet-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-violet-500/30 mx-auto">
              <svg
                className="w-8 h-8 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2.5}
                  d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                />
              </svg>
            </div>
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold mb-3">
            <span className="gradient-text">Verify Email</span>
          </h1>
          <p className="text-slate-600 text-lg mb-2">We've sent a verification code to</p>
          <p className="text-violet-600 font-semibold">{email}</p>
        </div>

        <div className="glass-effect rounded-3xl shadow-2xl border border-white/20 p-8">
          <Input
            label="Verification Code"
            type="text"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Enter 6-digit code"
            required
          />

          <Button
            onClick={handleVerify}
            variant="primary"
            size="lg"
            className="w-full"
            disabled={isLoading || !code.trim()}
          >
            {isLoading ? 'Verifying...' : 'Verify Email'}
          </Button>

          <div className="mt-6 text-center">
            <p className="text-sm text-slate-600">
              Didn't receive the code?{' '}
              <button className="text-violet-600 hover:text-violet-700 font-semibold">
                Resend
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
