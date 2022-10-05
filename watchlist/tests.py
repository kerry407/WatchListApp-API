from rest_framework.test import APITestCase 
from django.contrib.auth.models import User 
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from rest_framework import status


# Create your tests here.
class ModelSetup:
    
    def common_model_setup(self):
        """
        A model setup that can be used in multiple test usecases
        """
        self.user = User.objects.create_user(username="exampleuser", password="Akpororo1", email="exampleuser@gmail.com")
        self.stream_platform1 = StreamPlatform.objects.create(
                                                            name="IMDB", 
                                                            description="platform for streaming movies", 
                                                            website="www.imdb.com"
                                                            )
        self.stream_platform2 = StreamPlatform.objects.create(
                                                            name="Netflix", 
                                                            description="platform for streaming movies too", 
                                                            website="www.netflix.com"
                                                            )
        self.category1 = Category.objects.create(name="horror")
        self.category2 = Category.objects.create(name="Action")
        self.watchlist1 = WatchList.objects.create(
                                                title="The hulk",
                                                summary="the hulk movie",
                                                is_active=True,
                                                platform=self.stream_platform1
                                                )
        self.watchlist1.category.add(self.category1)
        self.watchlist2 = WatchList.objects.create(
                                                title="Aquaman",
                                                summary="the aquaman movie",
                                                is_active=True,
                                                platform=self.stream_platform2
                                                )
        self.watchlist1.category.add(self.category2)
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = self.refresh.access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        
class WatchListTestCase(ModelSetup, APITestCase):
    
    def setUp(self):
        return super().common_model_setup()
       
    def test_get_platform_list(self):
        response = self.client.get(reverse("streamplatform-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_individual_platform(self):
        response = self.client.get(reverse("streamplatform-detail", args=[self.stream_platform1.slug]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_platform_create(self):
        data = {
            "name": "spotify",
            "description": "stream music",
            "website": "www.spotify.com"
        }
        response = self.client.post(reverse("streamplatform-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_get_watchlist_list(self):
        response = self.client.get(reverse("watchlists"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_watchlist_detail(self):
        response = self.client.get(reverse("watchlist-detail", args=[self.watchlist1.slug]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_watchlist_create(self):
        data = {
            "title": "Superwoman",
            "summary": "superwoman",
            "is_active": True,
            "platform": self.stream_platform1,
            "category": [self.category1]
        }
        response = self.client.post(reverse("watchlists"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

class ReviewTestCase(ModelSetup, APITestCase):
    def setUp(self):
        return super().common_model_setup()
        
    def test_review_create(self):
        data = {
            "rating": 4.1,
            "body": "nice movie"
        }
        response = self.client.post(reverse("create-review", args=[self.watchlist1.slug]), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    
class CategoryTestCase(ModelSetup, APITestCase):
    def setUp(self):
        return super().common_model_setup()
    
    def test_category_list(self):
        response = self.client.get(reverse("category-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_category_detail(self):
        response = self.client.get(reverse("category-detail", args=[self.category2.slug]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_category_create(self):
        data = {"name": "Drama"}
        response = self.client.post(reverse("category-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

        