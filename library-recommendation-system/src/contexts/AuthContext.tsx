import { useEffect, useState, ReactNode } from 'react';
import {
  signIn,
  signOut,
  signUp,
  getCurrentUser,
  fetchUserAttributes,
  fetchAuthSession,
} from 'aws-amplify/auth';
import { useNavigate } from 'react-router-dom';
import { AuthContext, User } from './auth';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    checkUser();
  }, []);

  const checkUser = async () => {
    try {
      const currentUser = await getCurrentUser();
      const attributes = await fetchUserAttributes();
      const session = await fetchAuthSession();

      console.log('Current user:', currentUser);
      console.log('User attributes:', attributes);

      // Set user if they exist and are verified
      if (currentUser && attributes.email) {
        // Check if email is verified (Cognito returns string 'true')
        const isEmailVerified = attributes.email_verified === 'true';

        if (isEmailVerified) {
          // Check if user is in admin group
          const groups = session.tokens?.idToken?.payload['cognito:groups'] as string[] | undefined;
          const isAdmin = groups?.includes('admin') || false;

          console.log('User groups:', groups);
          console.log('Is admin:', isAdmin);

          setUser({
            id: currentUser.userId,
            email: attributes.email,
            name: attributes.name || attributes.email.split('@')[0],
            role: isAdmin ? 'admin' : 'user',
          });
        } else {
          console.log('Email not verified, user needs to verify');
          setUser(null);
        }
      } else {
        setUser(null);
      }
    } catch (error) {
      console.log('No authenticated user:', error);
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      // First check if user is already signed in
      try {
        const currentUser = await getCurrentUser();
        if (currentUser) {
          console.log('User already signed in, signing out first');
          await signOut();
        }
      } catch {
        // No user signed in, continue with login
      }

      const res = await signIn({
        username: email,
        password,
      });

      console.log('Sign in result:', res);

      // Check if user needs to confirm signup
      if (res.nextStep?.signInStep === 'CONFIRM_SIGN_UP') {
        navigate('/verify', { state: { email } });
        return;
      }

      // Successful login - check user and navigate
      await checkUser();
      navigate('/');
    } catch (err) {
      console.error('Login error:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (email: string, password: string, name: string) => {
    setIsLoading(true);
    try {
      await signUp({
        username: email,
        password,
        options: {
          userAttributes: {
            email,
            name,
          },
        },
      });

      // Navigate to verification page after successful signup
      navigate('/verify', { state: { email } });
    } catch (err) {
      console.error('Signup error:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      await signOut();
      setUser(null);
      navigate('/login');
    } catch (err) {
      console.error('Logout error:', err);
      // Even if signOut fails, clear local state
      setUser(null);
      navigate('/login');
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        signup,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
