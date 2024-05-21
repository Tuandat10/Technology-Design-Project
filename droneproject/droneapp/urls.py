from django.urls import path
from . import views

urlpatterns = [
    path("Home/<int:id>", views.Home, name="Home"),
    path("Restaurants/<int:id>",views.Restaurants,name="Restaurants"),
    path("Cart/<int:id>",views.Cart,name="Cart"),
    path("Profile/<int:id>",views.Profile, name="Profile"),
    path("Menu/<str:pk>/<int:id>",views.Menu, name="Menu"),
    path("Shopping-Info/<int:id>",views.ShoppingInfo, name="Shopping-Info"),
    path("Address/<int:id>",views.Address, name="Address"),
    path("Add-address/<int:id>",views.AddAddress, name="Add-address"),
    path("Payment-no-card/<int:id>",views.PaymentNoCard, name="Payment-no-card"),
    path("Add-card/<int:id>",views.AddCard, name="Add-card"),
    path("Payment-have-card/<int:id>",views.PaymentCard, name="Payment-have-card"),
    path("Payment-success/<int:id>",views.PaymentSuccess, name="Payment-success"),
    path("Delivery/<int:id>",views.Delivery, name="Delivery"),
    path("My-address/<int:id>",views.MyAddresses, name="My-address"),
    path("Favourite/<int:id>",views.Favourites, name="Favourite"),
    path("My-order-history/<int:id>",views.OrderHistory, name="My-order-history"),
    path("Notification/<int:id>",views.Notifications, name="Notification"),
    path("Payment/<int:id>",views.Payment, name="Payment"),
    path("Settings/<int:id>",views.Settings, name="Settings"),
    path("Logout/<int:id>",views.Logout, name="Logout"),
    path("",views.Signin, name="Signin"),
    path("Categories/<str:pk>/<int:id>",views.Categories, name="Categories"),
    path("Signup/",views.Signup, name="Signup"),
    path("test/",views.test, name="test"),
]