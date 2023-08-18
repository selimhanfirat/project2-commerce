from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name = "followers")
    pass


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length = 512)
    price = models.IntegerField()
    image = models.ImageField(upload_to='listing_images')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "listings")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    

class Bid(models.Model):
    amount = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids_made')  # Add related_name
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')  # Add related_name
    highest_bid = models.BooleanField(default=False)

    def __str__(self):
        return f"Bid of {self.amount} by {self.bidder.username} on {self.listing.title}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_made')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.listing.title}"
    
    
