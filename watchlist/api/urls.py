from watchlist.api import views 
from django.urls import path, include
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register("streams", views.StreamPlatformView, basename="streamplatform")

urlpatterns = [
    path("watchlists/", views.WatchlistListView.as_view()),
    path("watchlist/<str:slug>/", views.WatchListDetailView.as_view()), 
    path("", include(routers.urls)),    
    path("watchlist/<str:slug>/reviews/", views.ReviewListView.as_view()),
    path("watchlist/<str:slug>/review/add/", views.ReviewCreateView.as_view()),
    path("watchlist/review/<int:pk>/", views.ReviewDetailView.as_view()),
    path("watchlist/reviews", views.UserReviewList.as_view())
]