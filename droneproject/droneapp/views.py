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
        print("a"*80)
        print(request.POST.get('cartItems'))
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
from django.contrib import messages
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from .models import Order_General, Order_Food, Restaurant_Order






from django.shortcuts import render, redirect
from .models import Restaurant

def register(request):
    if request.method == 'POST':
        name = request.POST.get('store_name')
        location = request.POST.get('store_address')
        menu_items = request.POST.getlist('menu_items[]')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        opening_time = request.POST.get('opening_time')
        closing_time = request.POST.get('closing_time')
        picture_link = request.POST.get('icon')
        if password == password2:
            if Restaurant.objects.filter(email=email).exists():
                print('Email is already taken')
                return redirect('Res-signup')
            else:
                user = Restaurant.objects.create(email=email, password=password, name=name, location=location, menu_items=menu_items, phone=phone, opening_time=opening_time, closing_time=closing_time, picture_link=picture_link)
                user.save()
                return redirect('Res-signin')
        else:
            messages.error(request, 'Password is not matching')
            return redirect('Res-signup')
    else:
        return render(request, 'Res-signup.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        if Restaurant.objects.filter(email=email, password=password).exists():
            restaurant = Restaurant.objects.get(email=email, password=password)
            id = restaurant.restaurant_id
            return redirect('Res-dashboard', id)
        else:
            messages.error(request, 'Email or Password is incorrect')
            return redirect('Res-signin')
    return render(request, 'Res-signin.html')

def dashboard(request, id):
    results = []
    restaurant_orders = Restaurant_Order.objects.filter(restaurant=id, status='New order')
    for restaurant_order in restaurant_orders:
        order_generals = restaurant_order.order
        order_food = Order_Food.objects.filter(order_generalid=order_generals.order_id, restaurant=id)
        total_quantity = sum(food.quantity for food in order_food)
        customer = order_generals.customer
        order_data = {
            'customer_name': customer.name,
            'time': order_generals.time_ordered,
            'price': order_generals.total_price,
            'total_quantity': total_quantity,
            'order_id': order_generals.order_id
        }
        results.append(order_data)
    number_of_orders = len(results)
    restaurant_ordernumber = Restaurant_Order.objects.filter(restaurant=id).first()
    number_new_orders = Order_General.objects.filter(status='New order',order_id=restaurant_ordernumber.order.order_id).count()
    number_preparing_orders = Order_General.objects.filter(status='Preparing',order_id=restaurant_ordernumber.order.order_id).count()
    number_ready_orders = Order_General.objects.filter(status='Ready',order_id=restaurant_ordernumber.order.order_id).count()
    number_delivering_orders = Order_General.objects.filter(status='Delivering',order_id=restaurant_ordernumber.order.order_id).count()
    number_delivered_orders = Order_General.objects.filter(status='Delivered',order_id=restaurant_ordernumber.order.order_id).count()
    number = {
        'number_new_orders': number_new_orders,
        'number_preparing_orders': number_preparing_orders,
        'number_ready_orders': number_ready_orders,
        'number_delivering_orders': number_delivering_orders,
        'number_delivered_orders': number_delivered_orders
    }

    return render(request, 'Res-dashboard.html', {'results': results, 'id': id, 'number_of_orders': number_of_orders, 'number': number})

def ritems(request):
    return render(request, 'Res-items.html')

def rneworder(request):
    return render(request, 'Res-neworder.html')

def rnewordernoti(request, id):
    results = {}
    if request.method == 'POST':
        if request.POST.get('decline'):
            order_id = request.POST.get('order_id')
            order = Order_General.objects.get(order_id=order_id)
            order.status = 'Cancelled'
            order.save()
            restaurant_orders = Restaurant_Order.objects.filter(order=order,status='New order')
            for restaurant_order in restaurant_orders:
                restaurant_order.status = 'Cancelled'
                restaurant_order.save()
        else:
            order_id = request.POST.get('order_id')
            order = Order_General.objects.get(order_id=order_id)
            order.status = 'Preparing'
            order.save()
            restaurant_orders = Restaurant_Order.objects.filter(order=order,status='New order')
            for restaurant_order in restaurant_orders:
                restaurant_order.status = 'Preparing'
                restaurant_order.save()
    
    number_of_orders = 0
    number_of_neworders = 0
    restaurant_orders = Restaurant_Order.objects.filter(restaurant=id, status='New order')
    for restaurant_order in restaurant_orders:
        order_generals = restaurant_order.order
        order_foods = Order_Food.objects.filter(order_generalid=order_generals.order_id, restaurant=id)
        for order_food in order_foods:
            order_id = order_food.order_generalid.order_id
            price_each_food = order_food.price
            food_name = order_food.food
            quantity_each_food = order_food.quantity
            order_data = {
            'food_name': food_name,
            'price_each_food': price_each_food,
            'quantity_each_food': quantity_each_food,
            'customer_name': restaurant_order.order.customer.name,
            'order_general_id': restaurant_order.order.order_id,
            'service_fee': restaurant_order.order.service_fee,
            'delivery_fee': restaurant_order.order.delivery_fee,
            'total_price': restaurant_order.order.total_price,
            'order_id': order_id,
            'time_ordered': order_generals.time_ordered
            }
            if order_id in results:
                results[order_id].append(order_data)
                for order_id, order_list in results.items():
                    total_quantity = sum(order['quantity_each_food'] for order in order_list)
                    results[order_id][0]['total_quantity'] = total_quantity
                    order_general_object = Order_General.objects.get(order_id=order_id)
                    order_general_object.total_quantity = total_quantity
                    order_general_object.save()
            else:
                results[order_id] = [order_data]
                for order_id, order_list in results.items():
                    total_quantity = sum(order['quantity_each_food'] for order in order_list)
                    results[order_id][0]['total_quantity'] = total_quantity
                    order_general_object = Order_General.objects.get(order_id=order_id)
                    order_general_object.total_quantity = total_quantity
                    order_general_object.save()
        print(results)
        number_of_orders = len(results)
        print(number_of_orders)
        number_of_neworders = 0
    restaurant_ordernumber = Restaurant_Order.objects.filter(restaurant=id).first()
    number_new_orders = Order_General.objects.filter(status='New order',order_id=restaurant_ordernumber.order.order_id).count()
    number_preparing_orders = Order_General.objects.filter(status='Preparing',order_id=restaurant_ordernumber.order.order_id).count()
    number_ready_orders = Order_General.objects.filter(status='Ready',order_id=restaurant_ordernumber.order.order_id).count()
    number_delivering_orders = Order_General.objects.filter(status='Delivering',order_id=restaurant_ordernumber.order.order_id).count()
    number_delivered_orders = Order_General.objects.filter(status='Delivered',order_id=restaurant_ordernumber.order.order_id).count()
    number = {
        'number_new_orders': number_new_orders,
        'number_preparing_orders': number_preparing_orders,
        'number_ready_orders': number_ready_orders,
        'number_delivering_orders': number_delivering_orders,
        'number_delivered_orders': number_delivered_orders
    }
    #copy
    return render(request, 'Res-neworder-noti.html', {'results': results, 'id': id, 'results': results, 'number': number})

    
def rpreparingorder (request, id):
    results = {}
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order_General.objects.get(order_id=order_id)
        order.status = 'Ready'
        order.save()
        restaurant_orders = Restaurant_Order.objects.filter(order=order)
        pick_up_time = request.POST.get('time')
        order.pickup_time = pick_up_time
        order.save()
        for restaurant_order in restaurant_orders:
            restaurant_order.status = 'Ready'
            restaurant_order.save()

    number_of_orders = 0
    restaurant_orders = Restaurant_Order.objects.filter(restaurant=id, status='Preparing')
    for restaurant_order in restaurant_orders:
        order_generals = restaurant_order.order
        order_foods = Order_Food.objects.filter(order_generalid=order_generals.order_id, restaurant=id)
        for order_food in order_foods:
            order_id = order_food.order_generalid.order_id
            price_each_food = order_food.price
            food_name = order_food.food
            quantity_each_food = order_food.quantity
            order_data = {
            'food_name': food_name,
            'price_each_food': price_each_food,
            'quantity_each_food': quantity_each_food,
            'customer_name': restaurant_order.order.customer.name,
            'order_general_id': restaurant_order.order.order_id,
            'service_fee': restaurant_order.order.service_fee,
            'delivery_fee': restaurant_order.order.delivery_fee,
            'total_price': restaurant_order.order.total_price,
            'order_id': order_id
            }
            if order_id in results:
                results[order_id].append(order_data)
                for order_id, order_list in results.items():
                    total_quantity = sum(order['quantity_each_food'] for order in order_list)
                    results[order_id][0]['total_quantity'] = total_quantity
            else:
                results[order_id] = [order_data]
                for order_id, order_list in results.items():
                    total_quantity = sum(order['quantity_each_food'] for order in order_list)
                    results[order_id][0]['total_quantity'] = total_quantity
            
        print(results)
        number_of_orders = len(results)
        print(number_of_orders)

    result_neworder_noti = []
    restaurant_orders = Restaurant_Order.objects.filter(restaurant=id, status='New order')
    for restaurant_order in restaurant_orders:
        order_generals = restaurant_order.order
        order_food = Order_Food.objects.filter(order_generalid=order_generals.order_id, restaurant=id)
        total_quantity = sum(food.quantity for food in order_food)
        customer = order_generals.customer
        order_data = {
            'customer_name': customer.name,
            'time': order_generals.time_ordered,
            'price': order_generals.total_price,
            'total_quantity': total_quantity,
            'order_id': order_generals.order_id
        }
        result_neworder_noti.append(order_data)
    number_of_neworders = len(result_neworder_noti)
    restaurant_ordernumber = Restaurant_Order.objects.filter(restaurant=id).first()
    number_new_orders = Order_General.objects.filter(status='New order',order_id=restaurant_ordernumber.order.order_id).count()
    number_preparing_orders = Order_General.objects.filter(status='Preparing',order_id=restaurant_ordernumber.order.order_id).count()
    number_ready_orders = Order_General.objects.filter(status='Ready',order_id=restaurant_ordernumber.order.order_id).count()
    number_delivering_orders = Order_General.objects.filter(status='Delivering',order_id=restaurant_ordernumber.order.order_id).count()
    number_delivered_orders = Order_General.objects.filter(status='Delivered',order_id=restaurant_ordernumber.order.order_id).count()
    number = {
        'number_new_orders': number_new_orders,
        'number_preparing_orders': number_preparing_orders,
        'number_ready_orders': number_ready_orders,
        'number_delivering_orders': number_delivering_orders,
        'number_delivered_orders': number_delivered_orders
    }

    return render(request, 'Res-preparing-order.html', {'results': results, 'id': id, 'number': number})


def rorderready(request, id):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order_General.objects.get(order_id=order_id)
        order.status = 'Delivering'
        order.save()
        restaurant_orders = Restaurant_Order.objects.filter(order=order)
        for restaurant_order in restaurant_orders:
            restaurant_order.status = 'Delivering'
            restaurant_order.save()
    ready_results = {}
    restaurant_orders = Restaurant_Order.objects.filter(restaurant=id, status='Ready')
    for restaurant_order in restaurant_orders:
        order_generals = restaurant_order.order
        order_id = order_generals.order_id
        order_data = {
            'order_id': order_id,
            'customer_name': order_generals.customer.name,
            'time': order_generals.pickup_time,
            'total_quantity': order_generals.total_quantity,
            'price': order_generals.total_price
        }
        if order_id in ready_results:
            ready_results[order_id].append(order_data)
        else :
            ready_results[order_id] = [order_data]
    restaurant_ordernumber = Restaurant_Order.objects.filter(restaurant=id).first()
    number_new_orders = Order_General.objects.filter(status='New order',order_id=restaurant_ordernumber.order.order_id).count()
    number_preparing_orders = Order_General.objects.filter(status='Preparing',order_id=restaurant_ordernumber.order.order_id).count()
    number_ready_orders = Order_General.objects.filter(status='Ready',order_id=restaurant_ordernumber.order.order_id).count()
    number_delivering_orders = Order_General.objects.filter(status='Delivering',order_id=restaurant_ordernumber.order.order_id).count()
    number_delivered_orders = Order_General.objects.filter(status='Delivered',order_id=restaurant_ordernumber.order.order_id).count()
    number = {
        'number_new_orders': number_new_orders,
        'number_preparing_orders': number_preparing_orders,
        'number_ready_orders': number_ready_orders,
        'number_delivering_orders': number_delivering_orders,
        'number_delivered_orders': number_delivered_orders
    }

    return render(request, 'Res-order-ready.html', {'id': id, 'ready_results': ready_results, 'number': number})

def rorderdelivery (request, id):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order_General.objects.get(order_id=order_id)
        order.status = 'Delivered'
        order.save()
        restaurant_orders = Restaurant_Order.objects.filter(order=order)
        for restaurant_order in restaurant_orders:
            restaurant_order.status = 'Delivered'
            restaurant_order.save()
    delivery_results = {}
    restaurant_orders = Restaurant_Order.objects.filter(restaurant=id, status='Delivering')
    for restaurant_order in restaurant_orders:
        order_generals = restaurant_order.order
        order_id = order_generals.order_id
        order_data = {
            'order_id': order_id,
            'customer_name': order_generals.customer.name,
            'time': order_generals.pickup_time,
            'total_quantity': order_generals.total_quantity,
            'price': order_generals.total_price
        }
        if order_id in delivery_results:
            delivery_results[order_id].append(order_data)
        else :
            delivery_results[order_id] = [order_data]
    print(delivery_results)
    restaurant_ordernumber = Restaurant_Order.objects.filter(restaurant=id).first()
    number_new_orders = Order_General.objects.filter(status='New order',order_id=restaurant_ordernumber.order.order_id).count()
    number_preparing_orders = Order_General.objects.filter(status='Preparing',order_id=restaurant_ordernumber.order.order_id).count()
    number_ready_orders = Order_General.objects.filter(status='Ready',order_id=restaurant_ordernumber.order.order_id).count()
    number_delivering_orders = Order_General.objects.filter(status='Delivering',order_id=restaurant_ordernumber.order.order_id).count()
    number_delivered_orders = Order_General.objects.filter(status='Delivered',order_id=restaurant_ordernumber.order.order_id).count()
    number = {
        'number_new_orders': number_new_orders,
        'number_preparing_orders': number_preparing_orders,
        'number_ready_orders': number_ready_orders,
        'number_delivering_orders': number_delivering_orders,
        'number_delivered_orders': number_delivered_orders
    }

    return render(request, 'Res-order-delivery.html', {'id': id, 'delivery_results': delivery_results, 'number': number})
    
def rordertracking(request, id):

    order_tracking ={}
    restaurant_orders = Restaurant_Order.objects.filter(restaurant=id, status='Delivered')
    for restaurant_order in restaurant_orders:
        order_generals = restaurant_order.order
        order_id = order_generals.order_id
        order_data = {
            'order_id': order_id,
            'pickup_time': order_generals.pickup_time,
            'status': order_generals.status,
        }

        if order_id in order_tracking:
            order_tracking[order_id].append(order_data)
        else :
            order_tracking[order_id] = [order_data]
    restaurant_ordernumber = Restaurant_Order.objects.filter(restaurant=id).first()
    number_new_orders = Order_General.objects.filter(status='New order',order_id=restaurant_ordernumber.order.order_id).count()
    number_preparing_orders = Order_General.objects.filter(status='Preparing',order_id=restaurant_ordernumber.order.order_id).count()
    number_ready_orders = Order_General.objects.filter(status='Ready',order_id=restaurant_ordernumber.order.order_id).count()
    number_delivering_orders = Order_General.objects.filter(status='Delivering',order_id=restaurant_ordernumber.order.order_id).count()
    number_delivered_orders = Order_General.objects.filter(status='Delivered',order_id=restaurant_ordernumber.order.order_id).count()
    number = {
        'number_new_orders': number_new_orders,
        'number_preparing_orders': number_preparing_orders,
        'number_ready_orders': number_ready_orders,
        'number_delivering_orders': number_delivering_orders,
        'number_delivered_orders': number_delivered_orders
    }

    return render(request, 'Res-order-tracking.html', {'id': id, 'number': number, 'order_tracking': order_tracking})