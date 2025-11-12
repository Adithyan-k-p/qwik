from django.test import TestCase

# # Create your tests here.


from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Follow

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.role, 'user')

class UserAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_register(self):
        data = {'username': 'newuser', 'email': 'new@example.com', 'password': 'newpass123', 'password2': 'newpass123'}
        response = self.client.post('/api/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_login(self):
        data = {'email': 'test@example.com', 'password': 'testpass123'}
        response = self.client.post('/api/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_profile_update(self):
        data = {'bio': 'Updated bio!'}
        response = self.client.put('/api/users/me/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, 'Updated bio!')