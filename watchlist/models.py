from django.db import models
from django.contrib.auth.models import User 
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone 
# Create your models here.

class StreamPlatform(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    website = models.URLField() 
    image = models.ImageField(upload_to="streams/images", null=True, blank=True)
    slug = models.SlugField(db_index=True, editable=False, null=False, default='')
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name 
    

class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(db_index=True, editable=False, null=False, default='')
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name 

    class Meta:
        verbose_name_plural = "Categories"

class WatchList(models.Model):
    title = models.CharField(max_length=100, null=True)
    average_rating = models.FloatField(default=0)
    no_of_reviews = models.PositiveIntegerField(default=0)
    summary = models.TextField(max_length=1050, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    date_created = models.DateField(default=timezone.now)
    slug = models.SlugField(db_index=True, editable=False, null=False, default='')
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, null=True, related_name='watchlists')
    image = models.ImageField(upload_to="watchlist/images", null=True, blank=True)
    trailer = models.FileField(upload_to="watchlist/videos", null=True, blank=True)
    category = models.ManyToManyField(Category)
    
    class Meta:
        ordering = ("date_created",)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title 
    

class Review(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=250, null=True)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(default=timezone.now)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')
    
    class Meta:
        ordering = ("created_on",)
    
    def __str__(self):
        return f"Review by {self.created_by} about {self.watchlist.title}"


class UsersWatchList(models.Model):
    updated_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watchlist = models.ManyToManyField(WatchList, blank=True)
    
    def __str__(self):
        watchlist_count = self.watchlist.count()
        return f"{watchlist_count} watchlists added by {self.user.username}"