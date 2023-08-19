from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name = "followers")
    pass


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length = 512)
    price = models.IntegerField()
    image = models.ImageField(upload_to='listing_images/normal')
    larger_image = models.ImageField(upload_to = "listing_images/larger", null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "listings")
    created_at = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default = False)
    winning_bid = models.ForeignKey("Bid", null = True, blank = True, on_delete = models.SET_NULL, related_name= "won")
    categories = models.ManyToManyField("Category", related_name="listings")
    def __str__(self):
        return self.title

    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
     
    

class Bid(models.Model):
    amount = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids_made')  
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')

    def __str__(self):
        return f"Bid of {self.amount} by {self.bidder.username} on {self.listing.title}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_made')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.listing.title}"
    
    
