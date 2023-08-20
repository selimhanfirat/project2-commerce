from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.core.files import File
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from .models import Listing, Bid, Category, Comment
from django.conf import settings
from PIL import Image  # Import Pillow
import uuid
import os
from django.core.files.storage import default_storage
from .models import User

class New_Listing_Form(forms.Form):
    title = forms.CharField(label="Title", required=True)
    description = forms.CharField(label="Product Description", required=True)
    price = forms.IntegerField(label="Starting Bid", required=True)
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Categories",
        required=False
    )
    image = forms.ImageField(label="Product Photo", required=True)


def index(request):
    active_listings = Listing.objects.filter(closed=False)
    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# ... your other imports ...

@login_required 
def new_listing(request):
    if request.method == "GET":
        return render(request, "auctions/new_listing.html", {
            "form": New_Listing_Form()
        })
    elif request.method == "POST":
        user = request.user
        form = New_Listing_Form(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            title = cleaned_data["title"]
            description = cleaned_data["description"]
            price = cleaned_data["price"]
            
            # Get the currently logged-in user as the owner
            owner = request.user
            
            image = cleaned_data["image"]
            
            # Create the new listing with owner and creation time
            new_listing = Listing.objects.create(
                title=title,
                description=description,
                price=price,
                image=image,
                owner=owner,
                created_at=datetime.now(),  # Set the current time
            )
            
            for category in form.cleaned_data["categories"]:
                new_listing.categories.add(category)
            new_listing.save()

            
            # Resize the uploaded image using Pillow
            if new_listing.image:
                img = Image.open(new_listing.image.path)
                desired_size = (400, 400)  # Set your desired size here
                img.thumbnail(desired_size)
                img.save(new_listing.image.path)

                larger_img = img.resize((500, 500))  # Set the larger size here
                
                # Generate a unique identifier
                unique_id = uuid.uuid4().hex
                
                # Create filenames for normal and larger images with the unique identifier
                normal_image_filename = f"normal_{unique_id}.jpg"
                larger_image_filename = f"larger_{unique_id}.jpg"
                
                # Create filenames for normal and larger images with the unique identifier
                normal_image_filename = f"normal_{unique_id}.jpg"
                larger_image_filename = f"larger_{unique_id}.jpg"

                normal_image_path = os.path.join(settings.MEDIA_ROOT, 'listing_images', 'normal', normal_image_filename)
                larger_image_path = os.path.join(settings.MEDIA_ROOT, 'listing_images', 'larger', larger_image_filename)

                # Save images with the unique filenames
                img.save(normal_image_path)
                larger_img.save(larger_image_path)

                # Delete the original image
                default_storage.delete(new_listing.image.path)

                # Update the ImageField instances with the new filenames
                new_listing.image = os.path.join('listing_images', 'normal', normal_image_filename)
                new_listing.larger_image = os.path.join('listing_images', 'larger', larger_image_filename)

                # Save the new_listing object with the updated image fields
                new_listing.save()
            
            user.watchlist.add(new_listing)
            user.save()
            
            # Redirect to a success page or the new listing's detail page
            return HttpResponseRedirect(reverse("listing", args=[new_listing.pk]))
    
    return render(request, "auctions/new_listing.html", {
        "form": form
    })


            
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing 
    })

@login_required
def add_to_watchlist(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        
        if listing not in user.watchlist.all():
            user.watchlist.add(listing)
            user.save()
        
    return HttpResponseRedirect(reverse('watchlist', args=[user.id]))   

@login_required
def watchlist(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, "auctions/watchlist.html", {
        "watchlist": user.watchlist.all()
    })
        
@login_required
def bid(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        bid_amount = int(request.POST["bid_amount"])
        
        #handle the case where the owner bids on their own listing
        if listing.owner == request.user:
            messages.error(request, "You cannot bid on your own listing")
            return HttpResponseRedirect(reverse('listing', args=[listing.id]))
        

        if bid_amount > listing.price:
            # Create a new Bid instance
            new_bid = Bid(amount=bid_amount, bidder=request.user, listing=listing)
            new_bid.save()

            # Update the winning_bid field in the Listing model
            listing.winning_bid = new_bid
            listing.save()
            if listing not in user.watchlist.all():
                user.watchlist.add(listing)
                user.save()
            return HttpResponseRedirect(reverse('listing', args=[listing.id]))
        else:
            messages.error(request, "Bid amount must be higher than the current highest bid.")
            return HttpResponseRedirect(reverse('listing', args=[listing.id]))

    return HttpResponseRedirect(reverse('listing', args=[listing_id]))


@login_required
def listing_close(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk = listing_id)
        if listing.owner == request.user:
            listing.closed = True
            listing.save()
            return HttpResponseRedirect(reverse('listing', args=[listing.id]))
        else:
            messages.error(request, "You cannot close this listing because it's not yours")
            return HttpResponseRedirect(reverse('listing', args=[listing.id]))
    else:
        return HttpResponseRedirect(reverse('listing', args=[listing.id]))


def remove_from_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user

        if listing in user.watchlist.all():
            user.watchlist.remove(listing)
            user.save()

    return HttpResponseRedirect(reverse('watchlist', args=[user.id]))

def category_listings(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    listings = Listing.objects.filter(categories=category, closed=False)
    
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })
    
def comment(request, listing_id):
    if request.method == "POST":
        text = request.POST["text"]
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        new_comment = Comment.objects.create(
            text=text,
            author=user,
            listing=listing,
            created_at=datetime.now()  # Set the current time
        )
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))

    # Handle the GET request
    listing = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing
    })

            
    

def delete(request):
    # Delete all listings from the database
    Listing.objects.all().delete()

    # Delete all files in the media directory except the directories
    media_root = settings.MEDIA_ROOT
    for root, dirs, files in os.walk(media_root):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    # Redirect to a relevant page after deletion
    return HttpResponseRedirect(reverse("index"))