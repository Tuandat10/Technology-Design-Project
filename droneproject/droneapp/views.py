from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import auth
from django.contrib import messages
import json

def Home(request,id):
    customers = Customer.objects.filter(customer_id=id).first()
    id = customers.customer_id
    restaurants = Restaurant.objects.all()
    foods = Food.objects.all()[:8]
    return render(request,'Home.html',{'foods':foods,'restaurants':restaurants,'id':id})
def Restaurants(request,id):
    restaurants = Restaurant.objects.all()
    return render(request,"Restaurants.html",{ 'restaurants':restaurants,'id':id})
def Cart(request,id):
    return render(request,"Cart.html",{'id':id})
def Profile(request,id):
    return render(request,"Profile.html",{'id':id})
def Menu(request,pk,id):
    restaurant = Restaurant.objects.filter(name=pk).first()
    restaurant_id = restaurant.restaurant_id
    foods = Food.objects.filter(restaurant=restaurant_id)
    return render(request,"Menu.html",{ 'restaurant':restaurant,'foods':foods,'id':id})
def ShoppingInfo(request,id):
    return render(request,"Shopping-Info.html",{'id':id})
def Address(request,id):
    deliveries = Customer_delivery.objects.filter(customer=id)
    customers = Customer.objects.filter(customer_id=id).first()
    return render(request,"Address.html",{'id':id,'customers':customers,'deliveries':deliveries})
def PaymentNoCard(request,id):
    payments = Paymentmethod.objects.filter(customer_id=id)
    return render(request,"Payment-no-card.html",{'id':id,'payments':payments})
def AddAddress(request,id):
    if request.method == "POST":
        street_name = request.POST.get('street_name')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        customer = Customer.objects.get(pk=id)
        delivery = Customer_delivery.objects.create(customer=customer, delivery_address=street_name, delivery_city=city, delivery_state = state,delivery_postcode=zip_code,delivery_phone=phone)
        delivery.save()
        return redirect('Address',id)
    else:
        return render(request,"Add-address.html",{'id':id})
def AddCard(request,id):
    if request.method == "POST":
        card_name = request.POST.get('card_name')
        card_number = request.POST.get('card_number')
        expire = request.POST.get('expire')
        cvc = request.POST.get('cvc')
        customer = Customer.objects.get(pk=id)
        payment = Paymentmethod.objects.create(customer_id=id, card_name=card_name,card_number=card_number,expiry_date=expire,cvc=cvc)
        payment.save()
        return redirect('Payment-no-card',id)
    return render(request,"Add-card.html",{'id':id})
def PaymentCard(request,id):
    payments = Paymentmethod.objects.filter(customer_id=id)
    return render(request,"Payment-have-card.html",{'id':id,'payments':payments})
def PaymentSuccess(request,id):
    if request.method == "POST":
        cartitems = json.loads(request.POST.get('cartItems'))
        street = request.POST.get('street')
        zip_code = request.POST.get('zip_code')
        total_price = float(request.POST.get('totalPrice'))
        delivery_fee = float(request.POST.get('deliveryfee'))
        city = request.POST.get('city')
        province = request.POST.get('province')
        servicefee = float(request.POST.get('servicefee'))
        phone = request.POST.get('phone')
        card_number = request.POST.get('payment_id')
        time_ordered = request.POST.get('time_ordered')
        customer = Customer.objects.get(pk=id)
        payment_object = Paymentmethod.objects.filter(card_number=card_number).first()
        payment = Paymentmethod.objects.get(pk=payment_object.payment_id)
        order_general = Order_General.objects.create(customer=customer,payment=payment,total_price=total_price,delivery_fee=delivery_fee,service_fee=servicefee,street=street,zip_code=zip_code,city=city,province=province,phone=phone,time_ordered=time_ordered)
        order_general.save()
        total_restaurantid =[]
        total_restaurant = []
        for item in cartitems:
            restaurant = item['restaurant']
            restaurant_id = int(restaurant.split('(')[1].split(')')[0])
            total_restaurantid.append(restaurant_id)
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            order_food = Order_Food.objects.create(restaurant=restaurant,order_generalid=order_general,food=item['name'],quantity=item['quantity'])
            order_food.save()
        for i in set(total_restaurantid):
            restaurant = Restaurant.objects.get(pk=i)
            restaurant_order = Restaurant_Order.objects.create(restaurant=restaurant,order=order_general,status='New order')
            restaurant_order.save()
            total_restaurant.append(restaurant)
        print('aaaaaaaa')
        print(total_restaurant)
        return render(request,'Payment-success.html',{'id':id,'order_general':order_general,'total_restaurant':total_restaurant})
    else:
        return render(request,"Payment-success.html",{'id':id})
def Delivery(request,id):

    return render(request,"Delivery.html",{'id':id})
def MyAddresses(request,id):
    return render(request,"My-address.html",{'id':id})
def Favourites(request,id):
    return render(request,"Favourite.html",{'id':id})
def OrderHistory(request,id):
    return render(request,"My-order-history.html",{'id':id})
def Notifications(request,id):
    return render(request,"Notification.html",{'id':id})
def Payment(request,id):
    return render(request,"Payment.html",{'id':id})
def Settings(request,id):
    return render(request,"Settings.html",{'id':id})
def Logout(request,id):
    return render(request,"Logout.html",{'id':id})
def Signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.objects.filter(email=email).first()
        if customer is not None:
            if customer.password == password:
                id = customer.customer_id
                return redirect('Home',id)
            else:
                messages.info(request,"Invalid credentials")
                return redirect('Signin')
        else:
            messages.info(request,"Invalid credentials")
            return redirect('Signin')        
    else:
        return render(request,"Login-(U).html")
def Categories(request,pk,id):
    if request.method == "GET":
        if request.GET.get('category')=='all':
            foods = Food.objects.all()
            return render(request,"Categories.html",{ 'foods':foods,'id':id})
        elif request.GET.get('category')=='fastfood':
            foods = Food.objects.filter(category="Fast Food")
            return render(request,"Categories.html",{ 'foods':foods,'id':id})
        elif request.GET.get('category')=='sushi':
            foods = Food.objects.filter(category="Sushi")
            return render(request,"Categories.html",{ 'foods':foods,'id':id})
        elif request.GET.get('category')=='asian':
            foods = Food.objects.filter(category="Asian")
            return render(request,"Categories.html",{ 'foods':foods,'id':id})
        elif request.GET.get('category')=='bubbletea':
            foods = Food.objects.filter(category="Bubble tea")
            return render(request,"Categories.html",{ 'foods':foods,'id':id})
        elif request.GET.get('category')=='bakery':
            foods = Food.objects.filter(category="Bakery")
            return render(request,"Categories.html",{ 'foods':foods,'id':id})
        elif request.GET.get('category')=='vegan':
            foods = Food.objects.filter(category="Vegan")
            return render(request,"Categories.html",{ 'foods':foods,'id':id})
        elif request.GET.get('category')=='coffee':
            foods = Food.objects.filter(category="Coffee")
            return render(request,"Categories.html",{ 'foods':foods,'id':id})
        elif request.GET.get('category')=='alcohol':
            foods = Food.objects.filter(category="Alcohol")
            return render(request,"Categories.html",{ 'foods':foods,'id':id})
        else:
            foods = Food.objects.filter(category="Ice cream")
            return render(request,"Categories.html",{ 'foods':foods,'id':id})
    else:
        foods = Food.objects.all()
        print("aaaaa")
        return render(request,"Categories.html",{ 'foods':foods,'id':id})
def Signup(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        postcode = request.POST.get('postcode')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            if Customer.objects.filter(email=email).exists():
                messages.info(request,"Email already exists")
                return redirect('Signup')
            else:
                customer = Customer.objects.create(name=firstname+ " " + lastname, phone= phone, address=address, city=city, state=state,postcode=postcode,email=email,password=password)
                customer.save()
                messages.info(request,"User successfully created")
                return redirect("Signin")
        else:
            messages.info(request,"Password not matching")
            return redirect('Signup')
    else:
        return render(request,"Signup-(U).html")

def test(request):
    from geopy.geocoders import Nominatim
    from geopy.distance import geodesic
    geolocator = Nominatim(user_agent="geoapiExercises")
    location1 = geolocator.geocode("728 Glenferrie Rd, Hawthorn VIC 3122")
    location2 = geolocator.geocode("88 Elizabeth St, Melbourne VIC 3000")
    point1 = (location1.latitude, location1.longitude)
    point2 = (location2.latitude, location2.longitude)
    print('point1:',point1)
    print('point2:',point2)
    print(geodesic(point1, point2).kilometers)
    return render(request,"test.html")