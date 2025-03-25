import apiClient from './client';

export const createBooking = async (bookingData: unknown) => {
  const response = await apiClient.post('/api/bookings/booking-list/', bookingData);
  return response.data;
};

export const getUserBookings = async () => {
  const response = await apiClient.get('/api/bookings/user-bookings/');
  return response.data;
};

export const getGuestBookings = async (email: string) => {
  const response = await apiClient.post('/api/bookings/guest-bookings/', { email });
  return response.data;
};

export const getBusinessHours = async () => {
  const response = await apiClient.get('/api/bookings/business-hours/');
  return response.data;
};

export const deleteBooking = async (id: number) => {
  const response = await apiClient.delete(`/api/bookings/booking-list/${id}/`);
  return response.data;
};

export const getPackages = async () => {
  const response = await apiClient.get('/api/bookings/packages/');
  return response.data;
};
