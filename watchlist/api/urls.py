from watchlist.api import views 
from django.urls import path, include
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register("streams", views.StreamPlatformView, basename="streamplatform")

urlpatterns = [
    path("watchlists/", views.WatchlistListView.as_view(), name="watchlists"),
    path("watchlist/<str:slug>/", views.WatchListDetailView.as_view(), name="watchlist-detail"), 
    path("", include(routers.urls)),    
    path("watchlist/<str:slug>/reviews/", views.ReviewListView.as_view(), name="watchlist-reviews"),
    path("watchlist/<str:slug>/review/add/", views.ReviewCreateView.as_view(), name="create-review"),
    path("watchlist/review/<int:pk>/", views.ReviewDetailView.as_view(), name="review-detail"),
    path("watchlist/reviews/", views.UserReviewList.as_view(), name="user-reviews"),
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path("category/<str:slug>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path("watchlist/category/<str:slug>/", views.WatchListByCategory.as_view(), name="category-watclist")
]