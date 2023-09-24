# from django.test import TestCase
# from django.urls import reverse
# from rest_framework.test import APIClient
# from rest_framework.authtoken.models import Token
# from .models import CustomUser
#
#
# class UserViewSetTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
#         self.token = Token.objects.create(user=self.user)
#
#     def test_register(self):
#         url = reverse('user-register')
#         data = {
#             'username': 'newuser',
#             'password': 'newpassword',
#             'first_name': 'New',
#             'last_name': 'User',
#             'date_of_birth': '2000-01-01'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(CustomUser.objects.count(), 2)
#         self.assertEqual(CustomUser.objects.get(username='newuser').username, 'newuser')
#
#     def test_login(self):
#         url = reverse('user-login')
#         data = {
#             'login': 'testuser',
#             'password': 'testpassword'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['result']['token'], str(self.token))
#
#     def test_login_fail(self):
#         url = reverse('user-login')
#         data = {
#             'login': 'wronguser',
#             'password': 'wrongpassword'
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, 400)
