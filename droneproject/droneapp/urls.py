from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home, name="Home"),
    path("Restaurants/",views.Restaurants,name="Restaurants"),
    path("Cart/",views.Cart,name="Cart"),
    path("Profile/",views.Profile, name="Profile"),
    path("Menu/",views.Menu, name="Menu"),
    path("Shopping-Info/",views.ShoppingInfo, name="Shopping-Info"),
    path("Address/",views.Address, name="Address"),
    path("Add-address/",views.AddAddress, name="Add-address"),
    path("Payment-no-card/",views.PaymentNoCard, name="Payment-no-card"),
    path("Add-card/",views.AddCard, name="Add-card"),
    path("Payment-have-card/",views.PaymentCard, name="Payment-have-card"),
    path("Payment-success/",views.PaymentSuccess, name="Payment-success"),
    path("Delivery/",views.Delivery, name="Delivery"),
    path("My-address/",views.MyAddresses, name="My-address"),
    path("Favourite/",views.Favourites, name="Favourite"),
    path("My-order-history/",views.OrderHistory, name="My-order-history"),
    path("Notification/",views.Notifications, name="Notification"),
    path("Payment/",views.Payment, name="Payment"),
    path("Settings/",views.Settings, name="Settings"),
    path("Logout/",views.Logout, name="Logout"),

]