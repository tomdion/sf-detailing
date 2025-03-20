import apiClient from './client';

export const register = async (userData: unknown) => {
  const response = await apiClient.post('/api/users/register/', userData);
  return response.data;
};

export const login = async (credentials: { email: string; password: string }) => {
  const response = await apiClient.post('/api/users/login/', credentials);
  return response.data;
};

export const verifyTwoFactor = async (verificationData: { email: string; code: string }) => {
  const response = await apiClient.post('/api/users/verify-2fa/', verificationData);
  return response.data;
};

export const logout = async () => {
  const response = await apiClient.post('/api/users/logout/');
  return response.data;
};

export const getUserInfo = async () => {
  const response = await apiClient.get('/api/users/user-info/');
  return response.data;
};
