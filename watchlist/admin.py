from django.contrib import admin
from .models import StreamPlatform, WatchList, Review
# Register your models here.


@admin.register(StreamPlatform)
class StreamPlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'website']
    list_display_links = ['name']

@admin.register(WatchList)
class WatchListAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active']
    list_display_links = ['title']
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'rating', 'created_on', 'updated_on']
    list_filter = ['created_by', 'created_on', 'rating']