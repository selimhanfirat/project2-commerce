from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name = "new_listing"),
    path("listings/<int:listing_id>/", views.listing, name="listing"),
    path("add_to_watchlist/<int:listing_id>/", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist/<int:user_id>",views.watchlist, name = "watchlist"),
    path("bid/<int:listing_id>", views.bid, name = "bid"),
    path("close/<int:listing_id>", views.listing_close, name = "listing_close"),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name = "remove_from_watchlist"),
    path('category_listings/<str:category_name>/', views.category_listings, name='category_listings'),
    path('comment/<int:listing_id>', views.comment, name = "comment"),
    path("delete", views.delete, name = "delete"),
    
    
]

