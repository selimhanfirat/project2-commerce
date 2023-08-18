from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from .models import Listing
from PIL import Image  # Import Pillow



from .models import User

class New_Listing_Form(forms.Form):
    title = forms.CharField(label="Title", required=True)
    description = forms.CharField(label="Product Description", required=True)
    price = forms.IntegerField(label="Starting Bid", required=True)
    image = forms.ImageField(label="Product Photo", required=True)


def index(request):
    listings = Listing.objects.all
    return render(request, "auctions/index.html",{
        "listings": listings 
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
                created_at=datetime.now()  # Set the current time
            )
            
            # Resize the uploaded image using Pillow
            if new_listing.image:
                img = Image.open(new_listing.image.path)
                desired_size = (400, 400)  # Set your desired size here
                img.thumbnail(desired_size)
                img.save(new_listing.image.path)
            
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

def add_to_watchlist(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        
        if listing not in user.watchlist.all():
            user.watchlist.add(listing)
            
        
    return HttpResponseRedirect(reverse('watchlist', args=[user.id]))   

def watchlist(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, "auctions/watchlist.html", {
        "watchlist": user.watchlist.all()
    })
        

def delete(request):
    # Retrieve all listings from the database
    listings = Listing.objects.all()


    for listing in listings:
        listing.delete()

    # Redirect to a relevant page after deletion
    return HttpResponseRedirect(reverse("index")) 