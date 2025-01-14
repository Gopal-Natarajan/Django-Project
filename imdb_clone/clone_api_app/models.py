from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator 
from django.contrib.auth.models import User

class StreamingPlatform(models.Model):
    streamplatform = models.CharField(max_length=200)
    about = models.CharField(max_length=500)
    website = models.URLField(max_length=500)
    
    def __str__(self):
        return self.streamplatform


class WatchList(models.Model):
    tittle = models.CharField(max_length=30)
    storyline = models.CharField(max_length=100)
    platform = models.ForeignKey(StreamingPlatform, on_delete=models.CASCADE, related_name='watchlist')
    avg_rating = models.FloatField(default=0)
    no_of_rating = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.tittle
    
class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=500, null=True, blank=True)
    watchlist = models.ForeignKey(WatchList, on_delete= models.CASCADE, related_name='reviews')
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.rating) + " | " + str(self.watchlist)