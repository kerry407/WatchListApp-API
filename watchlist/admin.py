from django.contrib import admin
from .models import StreamPlatform, WatchList, Review, Category
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
    list_display = ['created_by', 'rating', ]
    list_filter = ['created_by', 'rating']
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]