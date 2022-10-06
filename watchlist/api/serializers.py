from rest_framework import serializers
from watchlist.models import WatchList, StreamPlatform, Review, Category, UsersWatchList

class ReviewSerializer(serializers.ModelSerializer):
    watchlist_title = serializers.SerializerMethodField()
    created_by = serializers.StringRelatedField(read_only=True)
    
    def get_watchlist_title(self, obj):
        return obj.watchlist.title
    
    class Meta:
        model = Review 
        fields = ["created_by", "body", "rating", "watchlist_title"]
        
           
class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    platform_name = serializers.SerializerMethodField()
    
    class Meta:
        model = WatchList 
        exclude = ['id']
    
    def get_platform_name(self, obj):
        return obj.platform.name

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlists = WatchListSerializer(many=True, read_only=True)
    
    class Meta:
        model = StreamPlatform
        exclude = ["id"]
        
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category 
        fields = ["name"]
        

class UsersWatchListSerializer(serializers.ModelSerializer):
    watchlist_count = serializers.SerializerMethodField()
    user = serializers.StringRelatedField(read_only=True)
    watchlist = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = UsersWatchList
        fields = ["watchlist_count", "user", "watchlist"]
        
    def get_watchlist_count(self, obj):
        return obj.watchlist.count()
    