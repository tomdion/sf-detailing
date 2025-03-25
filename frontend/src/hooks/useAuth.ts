import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getUserInfo, logout } from '@/api/auth';
import { setCookie, deleteCookie } from 'cookies-next';

// Define a type for your user object based on your API response
interface User {
  id: number;
  email: string;
  username: string;
  // Add any other properties that your user object contains
}

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const loadUserData = async () => {
    try {
      const response = await getUserInfo();
      setUser(response);
    } catch (error) {
      console.log('Not authenticated', error);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUserData();
  }, []);

  const loginUser = (userData: User) => {
    setUser(userData);
    setCookie('isLoggedIn', 'true');
  };

  const logoutUser = async () => {
    try {
      await logout();
      setUser(null);
      deleteCookie('isLoggedIn');
      router.push('/');
    } catch (error) {
      console.error('Error during logout:', error);
    }
  };

  return { 
    user, 
    loading, 
    loginUser, 
    logoutUser, 
    refreshUser: loadUserData,
    isLoggedIn: !!user 
  };
};