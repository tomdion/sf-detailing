import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getUserInfo, logout } from '@/api/auth';
import { setCookie, deleteCookie, getCookie } from 'cookies-next';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    async function loadUserFromCookie() {
      try {
        const response = await getUserInfo();
        setUser(response);
      } catch (error) {
        console.log('Not authenticated');
      } finally {
        setLoading(false);
      }
    }
    
    loadUserFromCookie();
  }, []);

  const loginUser = (userData) => {
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

  return { user, loading, loginUser, logoutUser, isLoggedIn: !!user };
};
