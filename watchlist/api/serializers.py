from rest_framework import serializers
from watchlist.models import WatchList, StreamPlatform, Review

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
        