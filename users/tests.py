from rest_framework.test import APITestCase 
from django.contrib.auth.models import User 
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from rest_framework import status

# Create your tests here.

class UserTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="exampleuser", password="Akpororo1", email="exampleuser@gmail.com")
    
    def test_create_user(self):
        data = {
            "username": "exampleuser1",
            "email": "exampleuser1@gmail.com",
            "password": "Akpororo1",
            "password2": "Akpororo1"
        }
        response = self.client.post(reverse("create-account"), data)
        user_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return user_data["token"]["refresh"]

    def test_login(self):
        data = {
            "username": "exampleuser",
            "password": "Akpororo1"
        }
        response = self.client.post(reverse("token_obtain_pair"), data)
        tokens = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return tokens["refresh"]
        
    def test_refresh_token(self):
        data = {
            "refresh": self.test_login()
        }
        response = self.client.post(reverse("token_refresh"), data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        