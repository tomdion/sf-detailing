from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser

# Create your tests here.
class UserAPITest(APITestCase):
    
    def test_create_user(self):
        self.valid_payload = {
            'email':'johndoe@example.com',
            'username': 'johndoe',
            'password':'12345'
        }
        response = self.client.post('/api/users/register/', self.valid_payload, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_login_user(self):
        self.user = CustomUser.objects.create_user(email='johndoe@example.com', username='johndoe', password='12345')

        self.login_data = {
            'email':'johndoe@example.com',
            'password':'12345'
        }
        
        response = self.client.post('/api/users/login/', self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], self.user.username)
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)
        self.assertTrue(response.cookies['access_token']['httponly'])
        self.assertTrue(response.cookies['access_token']['secure'])
        self.assertEqual(response.cookies['access_token']['samesite'], 'None')
        self.assertTrue(response.cookies['refresh_token']['httponly'])
        self.assertTrue(response.cookies['refresh_token']['secure'])
        self.assertEqual(response.cookies['refresh_token']['samesite'], 'None')

    def test_invalid_login(self):
        invalid_data = {
            'email':'johndoe@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post('/api/users/login/', invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access_token', response.cookies)
        self.assertNotIn('refresh_token', response.cookies)

