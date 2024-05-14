from django.shortcuts import render
from .models import *

def Home(request):
    restaurants = Restaurant.objects.all()
    foods = Food.objects.all()[:8]
    return render(request,'Home.html',{'foods':foods,'restaurants':restaurants})
def Restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request,"Restaurants.html",{ 'restaurants':restaurants})
def Cart(request):
    return render(request,"Cart.html")
def Profile(request):
    return render(request,"Profile.html")
def Menu(request,pk):
    restaurant = Restaurant.objects.filter(name=pk).first()
    restaurant_id = restaurant.restaurant_id
    foods = Food.objects.filter(restaurant=restaurant_id)
    return render(request,"Menu.html",{ 'restaurant':restaurant,'foods':foods})
def ShoppingInfo(request):
    return render(request,"Shopping-Info.html")
def Address(request):
    return render(request,"Address.html")
def PaymentNoCard(request):
    return render(request,"Payment-no-card.html")
def AddAddress(request):
    return render(request,"Add-address.html")
def AddCard(request):
    return render(request,"Add-card.html")
def PaymentCard(request):
    return render(request,"Payment-have-card.html")
def PaymentSuccess(request):
    return render(request,"Payment-success.html")
def Delivery(request):
    return render(request,"Delivery.html")
def MyAddresses(request):
    return render(request,"My-address.html")
def Favourites(request):
    return render(request,"Favourite.html")
def OrderHistory(request):
    return render(request,"My-order-history.html")
def Notifications(request):
    return render(request,"Notification.html")
def Payment(request):
    return render(request,"Payment.html")
def Settings(request):
    return render(request,"Settings.html")
def Logout(request):
    return render(request,"Logout.html")
def Signin(request):
    return render(request,"Login-(U).html")
def Categories(request,pk):
    if request.method == "GET":
        if request.GET.get('category')=='all':
            foods = Food.objects.all()
            return render(request,"Categories.html",{ 'foods':foods})
        elif request.GET.get('category')=='fastfood':
            foods = Food.objects.filter(category="Fast Food")
            return render(request,"Categories.html",{ 'foods':foods})
        elif request.GET.get('category')=='sushi':
            foods = Food.objects.filter(category="Sushi")
            return render(request,"Categories.html",{ 'foods':foods})
        elif request.GET.get('category')=='asian':
            foods = Food.objects.filter(category="Asian")
            return render(request,"Categories.html",{ 'foods':foods})
        elif request.GET.get('category')=='bubbletea':
            foods = Food.objects.filter(category="Bubble tea")
            return render(request,"Categories.html",{ 'foods':foods})
        elif request.GET.get('category')=='bakery':
            foods = Food.objects.filter(category="Bakery")
            return render(request,"Categories.html",{ 'foods':foods})
        elif request.GET.get('category')=='vegan':
            foods = Food.objects.filter(category="Vegan")
            return render(request,"Categories.html",{ 'foods':foods})
        elif request.GET.get('category')=='coffee':
            foods = Food.objects.filter(category="Coffee")
            return render(request,"Categories.html",{ 'foods':foods})
        elif request.GET.get('category')=='alcohol':
            foods = Food.objects.filter(category="Alcohol")
            return render(request,"Categories.html",{ 'foods':foods})
        else:
            foods = Food.objects.filter(category="Ice cream")
            return render(request,"Categories.html",{ 'foods':foods})
    else:
        foods = Food.objects.all()
        print("aaaaa")
        return render(request,"Categories.html",{ 'foods':foods})
# Create your views here.
