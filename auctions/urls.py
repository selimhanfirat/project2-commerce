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
    path("delete", views.delete, name = "delete"),
]

