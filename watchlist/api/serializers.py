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
        














































































# class WatchListSerializer(serializers.Serializer):
#     title = serializers.CharField(validators=[title_length])
#     summary = serializers.CharField(required=False, allow_blank=True)
#     is_published = serializers.BooleanField(default=True)
    
#     def create(self, validated_data):
#         return WatchList.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.summary = validated_data.get('summary', instance.summary)
#         instance.is_published = validated_data.get('is_published', instance.is_published)
#         instance.save()
#         return instance
    
    # def validate_title(self, value):
    #     if len(value) > 100:
    #         raise serializers.ValidationError("WatchList title cannot be greater than 100 characters!")
    #     return value
    
    # def validate(self, data):
    #     if data['title'] == data['summary']:
    #         raise serializers.ValidationError("WatchList title and summary cannot be the same!")
    #     return data 