from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Booking, Package, BusinessHours
from users.models import CustomUser
import uuid
from datetime import time, timedelta, datetime

class BookingAPITest(APITestCase):
    
    def create_test_data(self):
        """Helper method to create test data instead of using setUp"""
        # Create test user
        self.user = CustomUser.objects.create_user(
            email='user@example.com',
            username='user',
            password='password123'
        )
        
        # Create admin user
        self.admin = CustomUser.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='password123',
            is_staff=True
        )
        
        # Get or create packages
        self.interior_package, _ = Package.objects.get_or_create(
            name='interior',
            defaults={
                'display_name': 'Interior',
                'price': 50.00,
                'description': 'Interior detailing service'
            }
        )
        
        self.exterior_package, _ = Package.objects.get_or_create(
            name='exterior',
            defaults={
                'display_name': 'Exterior',
                'price': 60.00,
                'description': 'Exterior detailing service'
            }
        )
        
        self.combined_package, _ = Package.objects.get_or_create(
            name='interior_exterior',
            defaults={
                'display_name': 'Interior + Exterior',
                'price': 100.00,
                'description': 'Complete interior and exterior detailing service'
            }
        )
        
        # Create business hours (Monday-Friday 9AM-9PM, Saturday-Sunday 3PM-9PM)
        for day in range(7):
            if day < 5:  # Monday-Friday
                opening_time = time(9, 0)  # 9 AM
            else:  # Saturday-Sunday
                opening_time = time(15, 0)  # 3 PM
                
            BusinessHours.objects.get_or_create(
                day=day,
                defaults={
                    'opening_time': opening_time,
                    'closing_time': time(21, 0),  # 9 PM
                    'is_open': True
                }
            )
        
        # Generate future test date (next Monday at 10 AM)
        today = timezone.now().date()
        days_ahead = 7 - today.weekday()  # Days until next Monday
        self.test_date = today + timedelta(days=days_ahead)
        self.test_time = time(10, 0)  # 10 AM
        
        # Test booking data
        self.valid_booking_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone_number': '1234567890',
            'date': self.test_date.isoformat(),
            'time': self.test_time.isoformat(),
            'package': self.interior_package.id,
            'vehicle': 'car'
        }
    
    def test_create_booking(self):
        """Test creating a valid booking"""
        self.create_test_data()
        
        response = self.client.post('/api/bookings/booking-list/', self.valid_booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check the booking was created with correct data
        booking = Booking.objects.last()  # Use last() instead of first() in case there are existing bookings
        self.assertEqual(booking.first_name, 'John')
        self.assertEqual(booking.package.id, self.interior_package.id)
        self.assertFalse(booking.confirmed)
        self.assertIsNotNone(booking.confirmation_token)
    
    def test_authenticated_user_booking(self):
        """Test booking creation for authenticated user"""
        self.create_test_data()
        
        # Login
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post('/api/bookings/booking-list/', self.valid_booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check the booking is associated with the user
        booking = Booking.objects.last()
        self.assertEqual(booking.user, self.user)
    
    def test_booking_outside_business_hours(self):
        """Test creating a booking outside business hours is rejected"""
        self.create_test_data()
        
        # Try booking on Monday at 8 AM (before opening)
        invalid_data = self.valid_booking_data.copy()
        invalid_data['time'] = time(8, 0).isoformat()
        
        response = self.client.post('/api/bookings/booking-list/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_booking_on_closed_day(self):
        """Test booking on a day when business is closed"""
        self.create_test_data()
        
        # Set Sunday to closed
        sunday_hours = BusinessHours.objects.get(day=6)  # Sunday
        sunday_hours.is_open = False
        sunday_hours.save()
        
        # Try to book on a Sunday
        sunday_date = self.test_date
        while sunday_date.weekday() != 6:  # Find next Sunday
            sunday_date += timedelta(days=1)
            
        sunday_data = self.valid_booking_data.copy()
        sunday_data['date'] = sunday_date.isoformat()
        
        response = self.client.post('/api/bookings/booking-list/', sunday_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("closed", str(response.data).lower())
    
    def test_booking_in_past(self):
        """Test booking dates in the past are rejected"""
        self.create_test_data()
        
        # Try booking for yesterday
        yesterday = timezone.now().date() - timedelta(days=1)
        past_data = self.valid_booking_data.copy()
        past_data['date'] = yesterday.isoformat()
        
        response = self.client.post('/api/bookings/booking-list/', past_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("past", str(response.data).lower())
    
    def test_booking_time_conflict(self):
        """Test time conflict validation"""
        self.create_test_data()
        
        # Create a booking
        first_booking = Booking.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
            phone_number='0987654321',
            date=self.test_date,
            time=self.test_time,
            package=self.interior_package,
            vehicle='car',
            confirmation_token=str(uuid.uuid4())
        )
        
        # Try to create another booking at the same time
        response = self.client.post('/api/bookings/booking-list/', self.valid_booking_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_booking_within_time_restriction(self):
        """Test time restriction based on package type"""
        self.create_test_data()
        
        # Create a booking at 10 AM
        first_booking = Booking.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
            phone_number='0987654321',
            date=self.test_date,
            time=self.test_time,  # 10 AM
            package=self.interior_package,
            vehicle='car',
            confirmation_token=str(uuid.uuid4())
        )
        
        # Try booking at 12 PM (within the 3-hour restriction for interior package)
        conflicting_data = self.valid_booking_data.copy()
        conflicting_data['time'] = time(12, 0).isoformat()  # 12 PM
        
        response = self.client.post('/api/bookings/booking-list/', conflicting_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("a booking already exists within the restricted time.", str(response.data).lower())
        
        # Try booking at 1:30 PM (just outside the 3-hour restriction)
        non_conflicting_data = self.valid_booking_data.copy()
        non_conflicting_data['time'] = time(13, 30).isoformat()  # 1:30 PM
        
        response = self.client.post('/api/bookings/booking-list/', non_conflicting_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_package_time_restrictions(self):
        """Test different time restrictions for different packages"""
        self.create_test_data()
        
        # Create exterior package booking at 2 PM
        ext_booking = Booking.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
            phone_number='0987654321',
            date=self.test_date,
            time=time(14, 0),  # 2 PM
            package=self.exterior_package,
            vehicle='car',
            confirmation_token=str(uuid.uuid4())
        )
        
        # Try booking at 2:30 PM (within 1-hour restriction for exterior)
        ext_conflict = self.valid_booking_data.copy()
        ext_conflict['time'] = time(14, 30).isoformat()  # 2:30 PM
        ext_conflict['package'] = self.interior_package.id
        
        response = self.client.post('/api/bookings/booking-list/', ext_conflict, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Try booking at 3:30 PM (outside 1-hour restriction for exterior)
        ext_no_conflict = self.valid_booking_data.copy()
        ext_no_conflict['time'] = time(15, 30).isoformat()  # 3:30 PM
        ext_no_conflict['package'] = self.interior_package.id
        
        response = self.client.post('/api/bookings/booking-list/', ext_no_conflict, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_confirm_booking(self):
        """Test confirming a booking with token"""
        self.create_test_data()
        
        # Create an unconfirmed booking
        booking = Booking.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number='1234567890',
            date=self.test_date,
            time=self.test_time,
            package=self.interior_package,
            vehicle='car',
            confirmation_token='test-token-123',
            confirmed=False
        )
        
        # Confirm the booking
        response = self.client.get('/api/bookings/confirm/?token=test-token-123')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check booking was confirmed
        booking.refresh_from_db()
        self.assertTrue(booking.confirmed)
    
    def test_confirm_booking_invalid_token(self):
        """Test confirming a booking with invalid token"""
        self.create_test_data()
        
        response = self.client.get('/api/bookings/confirm/?token=invalid-token')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_user_bookings_list(self):
        """Test retrieving a user's bookings"""
        self.create_test_data()
        
        # Create bookings for the user
        Booking.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number='1234567890',
            date=self.test_date,
            time=self.test_time,
            package=self.interior_package,
            vehicle='car',
            user=self.user,
            confirmation_token='token1'
        )
        
        Booking.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number='1234567890',
            date=self.test_date + timedelta(days=1),
            time=self.test_time,
            package=self.exterior_package,
            vehicle='suv',
            user=self.user,
            confirmation_token='token2'
        )
        
        # Create a booking for another user
        Booking.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
            phone_number='0987654321',
            date=self.test_date,
            time=self.test_time,
            package=self.interior_package,
            vehicle='car',
            user=self.admin,
            confirmation_token='token3'
        )
        
        # Login as user
        self.client.force_authenticate(user=self.user)
        
        # Get user's bookings
        response = self.client.get('/api/bookings/user-bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only user's bookings
    
    def test_guest_bookings_lookup(self):
        """Test looking up bookings as a guest"""
        self.create_test_data()
        
        # Create guest bookings (no user)
        for i in range(3):
            Booking.objects.create(
                first_name=f'Guest{i}',
                last_name='User',
                email='guest@example.com',  # Same email for all
                phone_number='1234567890',
                date=self.test_date + timedelta(days=i),
                time=self.test_time,
                package=self.interior_package,
                vehicle='car',
                confirmation_token=f'token{i}'
            )
        
        # Lookup guest bookings
        lookup_data = {'email': 'guest@example.com'}
        response = self.client.post('/api/bookings/guest-bookings/', lookup_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
    
    def test_guest_bookings_invalid_email(self):
        """Test guest lookup with invalid email"""
        self.create_test_data()
        
        lookup_data = {'email': 'nonexistent@example.com'}
        response = self.client.post('/api/bookings/guest-bookings/', lookup_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_admin_view_all_bookings(self):
        """Test admin access to all bookings"""
        self.create_test_data()
        
        # Create several bookings
        for i in range(5):
            Booking.objects.create(
                first_name=f'User{i}',
                last_name='Test',
                email=f'user{i}@example.com',
                phone_number='1234567890',
                date=self.test_date + timedelta(days=i),
                time=self.test_time,
                package=self.interior_package,
                vehicle='car',
                confirmation_token=f'token{i}'
            )
        
        # Try accessing as regular user (should be forbidden)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/bookings/booking-list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try accessing as admin
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/api/bookings/booking-list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 5)  # At least our 5 bookings
    
    def test_delete_booking_as_owner(self):
        """Test deleting a booking as the owner"""
        self.create_test_data()
        
        # Create booking with user
        booking = Booking.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number='1234567890',
            date=self.test_date + timedelta(days=5),  # Future date (for 24-hour check)
            time=self.test_time,
            package=self.interior_package,
            vehicle='car',
            user=self.user,
            confirmation_token='test-token'
        )
        
        # Login as user
        self.client.force_authenticate(user=self.user)
        
        # Delete booking
        response = self.client.delete(f'/api/bookings/booking-list/{booking.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Booking.DoesNotExist):
            Booking.objects.get(id=booking.id)
    
    def test_delete_booking_less_than_24h(self):
        """Test deletion is rejected if less than 24 hours before booking"""
        self.create_test_data()
        
        # Create booking for tomorrow (less than 24h away)
        tomorrow = timezone.now().date() + timedelta(days=1)
        booking = Booking.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number='1234567890',
            date=tomorrow,
            time=timezone.now().time(),
            package=self.interior_package,
            vehicle='car',
            user=self.user,
            confirmation_token='test-token'
        )
        
        # Login as user
        self.client.force_authenticate(user=self.user)
        
        # Try to delete booking
        response = self.client.delete(f'/api/bookings/booking-list/{booking.id}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(Booking.objects.filter(id=booking.id).exists(), [True])
    
    def test_delete_booking_as_admin(self):
        """Test deleting any booking as admin"""
        self.create_test_data()
        
        # Create booking with regular user
        booking = Booking.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number='1234567890',
            date=self.test_date + timedelta(days=5),
            time=self.test_time,
            package=self.interior_package,
            vehicle='car',
            user=self.user,
            confirmation_token='test-token'
        )
        
        # Login as admin
        self.client.force_authenticate(user=self.admin)
        
        # Delete booking
        response = self.client.delete(f'/api/bookings/booking-list/{booking.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Booking.DoesNotExist):
            Booking.objects.get(id=booking.id)
    
    def test_delete_booking_as_other_user(self):
        """Test user cannot delete another user's booking"""
        self.create_test_data()
        
        # Create another user
        other_user = CustomUser.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='password123'
        )
        
        # Create booking with other user
        booking = Booking.objects.create(
            first_name='Other',
            last_name='User',
            email='other@example.com',
            phone_number='1234567890',
            date=self.test_date + timedelta(days=5),
            time=self.test_time,
            package=self.interior_package,
            vehicle='car',
            user=other_user,
            confirmation_token='test-token'
        )
        
        # Login as user
        self.client.force_authenticate(user=self.user)
        
        # Try to delete other user's booking
        response = self.client.delete(f'/api/bookings/booking-list/{booking.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(Booking.objects.filter(id=booking.id).exists(), [True])
    
    def test_delete_booking_as_guest(self):
        """Test guest can delete their own booking using session"""
        self.create_test_data()
        
        # Create a guest booking
        booking = Booking.objects.create(
            first_name='Guest',
            last_name='User',
            email='guest@example.com',
            phone_number='1234567890',
            date=self.test_date + timedelta(days=5),
            time=self.test_time,
            package=self.interior_package,
            vehicle='car',
            confirmation_token='test-token'
        )
        
        # Set session email (normally done during booking creation)
        session = self.client.session
        session['booking_email'] = 'guest@example.com'
        session.save()
        
        # Try to delete booking
        response = self.client.delete(f'/api/bookings/booking-list/{booking.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Booking.DoesNotExist):
            Booking.objects.get(id=booking.id)
    
    def test_business_hours_api(self):
        """Test retrieving business hours"""
        self.create_test_data()
        
        response = self.client.get('/api/bookings/business-hours/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)  # 7 days of the week
        
        # Verify correct data format
        for day_data in response.data:
            self.assertIn('day', day_data)
            self.assertIn('day_name', day_data)
            self.assertIn('opening_time', day_data)
            self.assertIn('closing_time', day_data)
            self.assertIn('is_open', day_data)