from django.contrib import messages
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from .models import Order_General, Order_Food, Restaurant_Order

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
        icon = request.POST.get('icon')
        if password == password2:
            if Restaurant.objects.filter(email=email).exists():
                print('Email is already taken')
                return redirect('Res-signup')
            else:
                user = Restaurant.objects.create(email=email, password=password, name=name, location=location, menu_items=menu_items, phone=phone, opening_time=opening_time, closing_time=closing_time, icon=icon)
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

    number_new_orders = Order_General.objects.filter(status='New order').count()
    number_preparing_orders = Order_General.objects.filter(status='Preparing').count()
    number_ready_orders = Order_General.objects.filter(status='Ready').count()
    number_delivering_orders = Order_General.objects.filter(status='Delivering').count()
    number_delivered_orders = Order_General.objects.filter(status='Delivered').count()
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
    number_new_orders = Order_General.objects.filter(status='New order').count()
    number_preparing_orders = Order_General.objects.filter(status='Preparing').count()
    number_ready_orders = Order_General.objects.filter(status='Ready').count()
    number_delivering_orders = Order_General.objects.filter(status='Delivering').count()
    number_delivered_orders = Order_General.objects.filter(status='Delivered').count()
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

    number_new_orders = Order_General.objects.filter(status='New order').count()
    number_preparing_orders = Order_General.objects.filter(status='Preparing').count()
    number_ready_orders = Order_General.objects.filter(status='Ready').count()
    number_delivering_orders = Order_General.objects.filter(status='Delivering').count()
    number_delivered_orders = Order_General.objects.filter(status='Delivered').count()
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
    
    number_new_orders = Order_General.objects.filter(status='New order').count()
    number_preparing_orders = Order_General.objects.filter(status='Preparing').count()
    number_ready_orders = Order_General.objects.filter(status='Ready').count()
    number_delivering_orders = Order_General.objects.filter(status='Delivering').count()
    number_delivered_orders = Order_General.objects.filter(status='Delivered').count()
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

    number_new_orders = Order_General.objects.filter(status='New order').count()
    number_preparing_orders = Order_General.objects.filter(status='Preparing').count()
    number_ready_orders = Order_General.objects.filter(status='Ready').count()
    number_delivering_orders = Order_General.objects.filter(status='Delivering').count()
    number_delivered_orders = Order_General.objects.filter(status='Delivered').count()
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
    restaurant_orders = Restaurant_Order.objects.filter(restaurant=id, status='Delivering')
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

    number_new_orders = Order_General.objects.filter(status='New order').count()
    number_preparing_orders = Order_General.objects.filter(status='Preparing').count()
    number_ready_orders = Order_General.objects.filter(status='Ready').count()
    number_delivering_orders = Order_General.objects.filter(status='Delivering').count()
    number_delivered_orders = Order_General.objects.filter(status='Delivered').count()
    number = {
        'number_new_orders': number_new_orders,
        'number_preparing_orders': number_preparing_orders,
        'number_ready_orders': number_ready_orders,
        'number_delivering_orders': number_delivering_orders,
        'number_delivered_orders': number_delivered_orders
    }

    return render(request, 'Res-order-tracking.html', {'id': id, 'number': number, 'order_tracking': order_tracking})