from ast import Delete
from django.shortcuts import get_object_or_404 
from rest_framework.response import Response 
from rest_framework import (status, generics, viewsets)
from rest_framework.views import APIView 
from rest_framework.exceptions import ValidationError
from django.db.models import Avg 
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from watchlist.models import (Category, WatchList, StreamPlatform, Review)
from .pagination import CustomPagination
from .serializers import *
from .permissions import (ReviewUserOrReadOnly, AdminOrReadOnly, WatchlistUserOnly)
# Create your views here.


class WatchlistListView(generics.ListCreateAPIView):
    permission_classes = [AdminOrReadOnly]
    serializer_class = WatchListSerializer
    queryset = WatchList.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['platform__name', 'date_created', 'category__name']
    search_fields = ['title', 'platform__name', 'category__name']
    ordering_fields = ['average_rating', 'date_created']
    pagination_class = CustomPagination
    

class WatchListDetailView(APIView):
    permission_classes = [AdminOrReadOnly]
    
    def get_object(self, slug):
        return get_object_or_404(WatchList, slug=slug)   
    
    def get(self, request, slug):
        watchlist = self.get_object(slug)
        serializer = WatchListSerializer(watchlist)
        return Response(serializer.data)
     
    def put(self, request, slug):
        watchlist = self.get_object(slug)
        serializer = WatchListSerializer(watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, slug):
        watchlist = self.get_object(slug)
        watchlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class WatchListByCategory(generics.ListAPIView):
    serializer_class = WatchListSerializer
    
    def get_queryset(self):
        slug = self.kwargs["slug"]
        queryset = WatchList.objects.filter(category__slug=slug)
        return queryset
    
    
class StreamPlatformView(viewsets.ViewSet):
    lookup_field = "slug"
    permission_classes = [AdminOrReadOnly]
    
    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, slug):
        queryset = get_object_or_404(StreamPlatform, slug=slug)
        serializer = StreamPlatformSerializer(queryset)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, slug):
        queryset = get_object_or_404(StreamPlatform, slug=slug)
        serializer = StreamPlatformSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, slug):
        queryset = get_object_or_404(StreamPlatform, slug=slug)
        queryset.delete()
        msg = "Streaming Platform successfully deleted"
        return Response(msg, status=status.HTTP_204_NO_CONTENT)
        

class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer 
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination
    filterset_fields = ['created_by__username']
    
    def get_queryset(self):
        slug = self.kwargs["slug"]
        return Review.objects.filter(watchlist__slug=slug)

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer 
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        slug = self.kwargs.get("slug")
        watchlist = WatchList.objects.get(slug=slug)
        review_user = self.request.user
        review = Review.objects.filter(watchlist=watchlist, created_by=review_user)
        
        if review.exists():
            raise ValidationError("You have already made a review about this watchlist!")
        else:
            serializer.save(watchlist=watchlist, created_by=review_user)
            watchlist_review = Review.objects.filter(watchlist__slug=slug)
            average_rating = watchlist_review.aggregate(Avg("rating"))
            watchlist.average_rating = average_rating["rating__avg"]
            watchlist.no_of_reviews = watchlist_review.count()
            watchlist.save() 
        
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    
    

class UserReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer 
    
    def get_queryset(self):
        queryset = Review.objects.all()
        username = self.request.query_params.get("username")
        if username is not None:
            queryset = queryset.filter(created_by__username=username)
        return queryset
    

class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [AdminOrReadOnly]
    
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer 
    queryset = Category.objects.all()
    permission_classes = [AdminOrReadOnly]
    lookup_field = "slug"
    

class UsersWatchlistCreateView(generics.CreateAPIView):
    serializer_class = UsersWatchListSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        slug = self.kwargs["slug"]
        watchlist = WatchList.objects.get(slug=slug)
        saved_watchlist = watchlist.userswatchlist_set.filter(watchlist__slug=slug)

        try:
            user_watchlist = UsersWatchList.objects.get(user__id=self.request.user.pk)
            
            if not saved_watchlist:
                user_watchlist.watchlist.add(watchlist.pk)
                return Response({"msg": f"{watchlist.title} added to watchlist"}, status=status.HTTP_201_CREATED)
            else:
                user_watchlist.watchlist.remove(watchlist.pk)
                return Response({"msg": f"{watchlist.title} removed watchlist"}, status=status.HTTP_204_NO_CONTENT)
            
        except UsersWatchList.DoesNotExist:
            new_user_watchlist = UsersWatchList()
            new_user_watchlist.user = self.request.user 
            new_user_watchlist.save()
            new_user_watchlist.watchlist.add(watchlist.pk)
            return Response({"msg": f"{watchlist.title} added to watchlist"}, status=status.HTTP_201_CREATED)
        
            
            
class UserWatchlistListView(generics.ListAPIView):
    serializer_class = UsersWatchListSerializer
    permission_classes = [WatchlistUserOnly]
            
    def get_queryset(self):
    
        queryset = UsersWatchList.objects.filter(user__username=self.request.user.username)
        return queryset 
            
    
        
            