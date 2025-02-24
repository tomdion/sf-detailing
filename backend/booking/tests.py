from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Booking

# Create your tests here.
class BookingAPITest(APITestCase):

    def test_create_booking(self):
        self.valid_payload = {
            "id" : "1",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "phone_number": "1234567890",
            "date": "2025-02-25",
            "time": "14:00:00",
            "package": "interior",
            "vehicle": "car"
        }
        response = self.client.post('/api/bookings/booking-list/', self.valid_payload, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.get().id, 1)

    def test_duplicate_booking(self):
        self.valid_payload = {
            "id" : "1",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "phone_number": "1234567890",
            "date": "2025-02-25",
            "time": "14:00:00",
            "package": "interior",
            "vehicle": "car"
        }
        response = self.client.post('/api/bookings/booking-list/', self.valid_payload, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(Booking.objects.count(), 1)

    

    def test_malformed_booking(self):
        self.valid_payload = {
            "id" : "1",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "phone_number": "1234567890",
            "date": "hello, world",
            "time": "14:00:00",
            "package": "interior",
            "vehicle": "car"
        }

        response = self.client.post('/api/bookings/booking-list/')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_booking(self):
        response = self.client.get('/api/bookings/booking-list/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_delete_booking(self):
        self.valid_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "phone_number": "1234567890",
            "date": "2025-02-25",
            "time": "14:00:00",
            "package": "interior",
            "vehicle": "car"
        }
        response = self.client.delete('/api/bookings/booking-list/1/', self.valid_payload, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Booking.objects.count(), 0)