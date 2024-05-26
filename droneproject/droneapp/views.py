from django.shortcuts import render, redirect
import folium.plugins
from .models import *
from django.contrib.auth.models import auth
from django.contrib import messages
import json
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium, time
import openrouteservice

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
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        customer = Customer.objects.get(pk=id)
        customer.name = name
        customer.phone = phone
        customer.email = email
        customer.save()
        messages.info(request,"Profile updated successfully")
        return redirect('Profile',id)
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
        street = request.POST.get('street').strip()
        zip_code = request.POST.get('zip_code').strip()
        total_price = float(request.POST.get('totalPrice'))
        delivery_fee = float(request.POST.get('deliveryfee'))
        city = request.POST.get('city').strip()
        province = request.POST.get('province').strip()
        servicefee = float(request.POST.get('servicefee'))
        phone = request.POST.get('phone')
        card_number = request.POST.get('payment_id')
        time_ordered = request.POST.get('time_ordered')
        customer = Customer.objects.get(pk=id)
        payment_object = Paymentmethod.objects.filter(card_number=card_number).first()
        payment = Paymentmethod.objects.get(pk=payment_object.payment_id)
        order_general = Order_General.objects.create(customer=customer,payment=payment,total_price=total_price,delivery_fee=delivery_fee,service_fee=servicefee,street=street,zip_code=zip_code,city=city,province=province,phone=phone,time_ordered=time_ordered)
        order_general.save()
        print('*'*80)
        print(order_general.order_id)
        order_general_id = order_general.order_id
        total_restaurantid =[]
        total_restaurant = []
        total_weight = 0
        for item in cartitems:
            restaurant = item['restaurant']
            restaurant_id = int(restaurant.split('(')[1].split(')')[0])
            total_restaurantid.append(restaurant_id)
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            food_weight = Food.objects.get(food_name=item['name'],restaurant=restaurant).total_weight
            total_food_weight = food_weight * item['quantity']
            total_weight += total_food_weight
            order_food = Order_Food.objects.create(restaurant=restaurant,order_generalid=order_general,food=item['name'],quantity=item['quantity'],price=item['price']*item['quantity'])
            order_food.save()
        for i in set(total_restaurantid):
            restaurant = Restaurant.objects.get(pk=i)
            restaurant_order = Restaurant_Order.objects.create(restaurant=restaurant,order=order_general,status='New order')
            restaurant_order.save()
            total_restaurant.append(restaurant)
        address_customer = street + ", " + city + ", " + province + ", " + zip_code
        address_restaurant = total_restaurant[0].location
        return render(request,'Payment-success.html',{'id':id,'order_general':order_general,'total_restaurant':total_restaurant,"address_customer":address_customer,"address_restaurant":address_restaurant,"order_general_id":order_general_id,'total_weight':total_weight})
    else:
        return render(request,"Payment-success.html",{'id':id})
def Delivery(request,id):
    if request.method == "POST":
        geolocator = Nominatim(user_agent="YourAppName")
        address_customer = request.POST.get('address_customer')
        address_restaurant = request.POST.get('address_restaurant')
        order_general_id = request.POST.get('order_general_id')
        total_weight = request.POST.get('total_weight')
        order_general_object = Order_General.objects.get(order_id=order_general_id)
        location_customer = geolocator.geocode(address_customer)
        location_restaurant = geolocator.geocode(address_restaurant)
        chargingstations = ChargingStation.objects.all()
        min_distance = float('inf')
        nearest_station = None
        max_weight_perdrone = 10
        if float(total_weight) <= max_weight_perdrone:
            number_drone = 1
            numberdrone_status = True
            for chargingstation in chargingstations:
                # Geocode the charging station location
                location_charging = geolocator.geocode(chargingstation.location)

                # Calculate the distance to the restaurant
                distance = geodesic((location_charging.latitude, location_charging.longitude), (location_restaurant.latitude, location_restaurant.longitude)).kilometers
                if distance < min_distance:
                    min_distance = distance
                    nearest_station = location_charging
                    nearest_stationungeocode = chargingstation
                charginstationstatuses = ChargingStationStatus.objects.filter(station=nearest_stationungeocode,status = True)
                if charginstationstatuses.count() == 0:
                        min_distance = float('inf')
                else:
                    max_battery = -float('inf')
                    for chargingstationstatus in charginstationstatuses:
                        if chargingstationstatus.drone.battery_level > max_battery:
                            drone = chargingstationstatus.drone
                    charginestationstatus_drone = ChargingStationStatus.objects.get(drone=drone,station=nearest_stationungeocode,status=True)
                    charginestationstatus_drone.status = False
                    charginestationstatus_drone.save()
                    order_general_object = Order_General.objects.get(order_id=order_general_id)
                    order_general_object.drone = drone
                    order_general_object.save()
                    first_distance = geodesic((nearest_station.latitude, nearest_station.longitude), (location_restaurant.latitude, location_restaurant.longitude)).kilometers
                    second_distance = geodesic((location_restaurant.latitude, location_restaurant.longitude), (location_customer.latitude, location_customer.longitude)).kilometers
                    total_distance = first_distance + second_distance
                    third_distance = geodesic((location_customer.latitude, location_customer.longitude), (nearest_station.latitude, nearest_station.longitude)).kilometers
                    total_batteryused = (total_distance + third_distance) * 0.5
                    if drone.battery_level > total_batteryused:
                        drone.battery_level -= total_batteryused
                        drone.save()
                    else:
                        # In reality we will wait them to charge the drone
                        drone.battery_level = 100
                        drone.save()
                    flighpath = FlightPath.objects.create(start_location = address_restaurant,end_location = address_customer,drone = drone,battery_usage = total_batteryused)
                    flighpath.save()
                    order_general_status = None
                    if (order_general_object.status == 'New order') or (order_general_object.status == 'Preparing'):
                        # Geocode the customer and restaurant addresses
                        # Create the map and add the markers
                        m = folium.Map(location=[nearest_station.latitude, nearest_station.longitude], zoom_start=14)
                        print("*"*80)
                        print(nearest_station.latitude, nearest_station.longitude)
                        folium.Marker([nearest_station.latitude, nearest_station.longitude], popup='Charging Station').add_to(m)
                        folium.Marker([location_restaurant.latitude, location_restaurant.longitude], popup='Restaurant').add_to(m)
                        folium.Marker([location_customer.latitude, location_customer.longitude], popup='Customer').add_to(m)
                        # Calculate the route and add it to the map
                        client = openrouteservice.Client(key='5b3ce3597851110001cf62481f738855150c49b3b8e6addabb1c3f67')
                        coords = ((nearest_station.longitude, nearest_station.latitude), (location_restaurant.longitude, location_restaurant.latitude))
                        route = client.directions(coordinates=coords, profile='foot-hiking', format='geojson')
                        folium.plugins.AntPath(locations=[(coord[1], coord[0]) for coord in route['features'][0]['geometry']['coordinates']]).add_to(m)
                        m = m._repr_html_()
                        if order_general_object.status == 'New order':
                            order_general_status = 'New order'
                            return render(request,"Delivery.html",{'id':id, 'map': m,'order_general_status':order_general_status,'order_general_id':order_general_id,'total_weight':total_weight,"numberdrone_status":numberdrone_status,"number_drone":number_drone})
                        elif order_general_object.status == 'Preparing':
                            order_general_status = 'Preparing'
                            return render(request,"Delivery.html",{'id':id, 'map': m,'order_general_status':order_general_status,'order_general_id':order_general_id,'total_weight':total_weight,"numberdrone_status":numberdrone_status,"number_drone":number_drone})
                        elif order_general_object.status == "Delivering":
                            order_general_status = 'Delivering'
                            return render(request,"Delivery.html",{'id':id, 'map': m,'order_general_status':order_general_status,'order_general_id':order_general_id,'total_weight':total_weight,"numberdrone_status":numberdrone_status,"number_drone":number_drone})
                    else:
                        # Create the map and add the markers
                        m = folium.Map(location=[nearest_station.latitude, nearest_station.longitude], zoom_start=14)
                        folium.Marker([location_customer.latitude, location_customer.longitude], popup='Customer').add_to(m)
                        folium.Marker([nearest_station.latitude, nearest_station.longitude], popup='Charging Station').add_to(m)
                        folium.Marker([location_restaurant.latitude, location_restaurant.longitude], popup='Restaurant').add_to(m)
                        # Calculate the route and add it to the map
                        client = openrouteservice.Client(key='5b3ce3597851110001cf62481f738855150c49b3b8e6addabb1c3f67')
                        coords = ((location_customer.longitude, location_customer.latitude), (location_restaurant.longitude, location_restaurant.latitude))
                        route = client.directions(coordinates=coords, profile='foot-hiking', format='geojson')
                        folium.plugins.AntPath(locations=[(coord[1], coord[0]) for coord in route['features'][0]['geometry']['coordinates']]).add_to(m)
                        m = m._repr_html_() 
                        if order_general_object.status == "Ready":
                            order_general_status = 'Ready'
                            return render(request,"Delivery.html",{'id':id, 'map': m,'order_general_status':order_general_status,"order_general_id":order_general_id,'total_weight':total_weight,"numberdrone_status":numberdrone_status,"number_drone":number_drone})
                        elif order_general_object.status == "Delivering":
                            order_general_status = 'Delivering'
                            return render(request,"Delivery.html",{'id':id, 'map': m,'order_general_status':order_general_status,"order_general_id":order_general_id,'total_weight':total_weight,"numberdrone_status":numberdrone_status,"number_drone":number_drone})
                        else:
                            order_general_status = 'Delivered'
                            chargingstations = ChargingStation.objects.all()
                            min_distance = float('inf')
                            nearest_station = None
                            for chargingstation in chargingstations:
                                numberdrone = ChargingStationStatus.objects.filter(station=chargingstation,status = True).count()
                                if numberdrone < 10:
                                    # Geocode the charging station location
                                    location_charging = geolocator.geocode(chargingstation.location)
                                    # Calculate the distance to the restaurant
                                    distance = geodesic((location_charging.latitude, location_charging.longitude), (location_customer.latitude, location_customer.longitude)).kilometers
                                    if distance < min_distance:
                                        min_distance = distance
                                        nearest_station = chargingstation
                            chargingstationstatus = ChargingStationStatus.objects.create(drone=drone,station=nearest_station,status=True)
                            chargingstationstatus.save()
                            flighpath = FlightPath.objects.create(start_location = address_customer,end_location = nearest_station.location,drone = drone,battery_usage = third_distance*0.5)
                            flighpath.save()
                            drone.battery_level = 100
                            drone.save()                  
                            return render(request,"Delivery.html",{'id':id, 'map': m,'order_general_status':order_general_status,'order_general_id':order_general_id,'total_weight':total_weight,"numberdrone_status":numberdrone_status,"number_drone":number_drone})
        elif float(total_weight) > max_weight_perdrone and float(total_weight) <= 2*max_weight_perdrone:
            number_drone = 2
            numberdrone_status = True
            # drone 1
            for chargingstation in chargingstations:
                # Geocode the charging station location
                location_charging = geolocator.geocode(chargingstation.location)
                numberdrone = 0

                # Calculate the distance to the restaurant
                distance = geodesic((location_charging.latitude, location_charging.longitude), (location_restaurant.latitude, location_restaurant.longitude)).kilometers
                if distance < min_distance:
                    min_distance = distance
                    nearest_station = location_charging
                    nearest_stationungeocode = chargingstation
                charginstationstatuses = ChargingStationStatus.objects.filter(station=nearest_stationungeocode,status = True)
                if charginstationstatuses.count() == 0:
                        min_distance = float('inf')
                else:
                    max_battery = -float('inf')
                    # drone 1
                    for chargingstationstatus in charginstationstatuses:
                        if chargingstationstatus.drone.battery_level > max_battery:
                            drone = chargingstationstatus.drone
                    charginestationstatus_drone = ChargingStationStatus.objects.get(drone=drone,station=nearest_stationungeocode,status=True)
                    charginestationstatus_drone.status = False
                    charginestationstatus_drone.save()
                    order_general_object = Order_General.objects.get(order_id=order_general_id)
                    order_general_object.drone = drone
                    order_general_object.save()
                    first_distance = geodesic((nearest_station.latitude, nearest_station.longitude), (location_restaurant.latitude, location_restaurant.longitude)).kilometers
                    second_distance = geodesic((location_restaurant.latitude, location_restaurant.longitude), (location_customer.latitude, location_customer.longitude)).kilometers
                    total_distance = first_distance + second_distance
                    third_distance = geodesic((location_customer.latitude, location_customer.longitude), (nearest_station.latitude, nearest_station.longitude)).kilometers
                    total_batteryused = (total_distance + third_distance) * 0.5
                    if drone.battery_level > total_batteryused:
                        drone.battery_level -= total_batteryused
                        drone.save()
                    else:
                        # In reality we will wait them to charge the drone
                        drone.battery_level = 100
                        drone.save()
                    flighpath = FlightPath.objects.create(start_location = address_restaurant,end_location = address_customer,drone = drone,battery_usage = total_batteryused)
                    flighpath.save()
                    # drone2
                    for chargingstation in chargingstations:
                        # Geocode the charging station location
                        location_charging = geolocator.geocode(chargingstation.location)
                        numberdrone = 0
                        min_distance = float('inf')
                        # Calculate the distance to the restaurant
                        distance = geodesic((location_charging.latitude, location_charging.longitude), (location_restaurant.latitude, location_restaurant.longitude)).kilometers
                        if distance < min_distance:
                            min_distance = distance
                            nearest_station2 = location_charging
                            nearest_stationungeocode = chargingstation
                        charginstationstatuses = ChargingStationStatus.objects.filter(station=nearest_stationungeocode,status = True)
                        if charginstationstatuses.count() == 0:
                                print("*"*80)
                                print("go if")
                                min_distance = float('inf')
                        else:
                            max_battery = -float('inf')               
                            for chargingstationstatus in charginstationstatuses:
                                if chargingstationstatus.drone.battery_level > max_battery:
                                    drone2 = chargingstationstatus.drone
                            charginestationstatus_drone = ChargingStationStatus.objects.get(drone=drone2,station=nearest_stationungeocode,status=True)
                            charginestationstatus_drone.status = False
                            charginestationstatus_drone.save()
                            order_general_object = Order_General.objects.get(order_id=order_general_id)
                            order_general_object.drone = drone2
                            order_general_object.save()
                            first_distance = geodesic((nearest_station2.latitude, nearest_station2.longitude), (location_restaurant.latitude, location_restaurant.longitude)).kilometers
                            second_distance = geodesic((location_restaurant.latitude, location_restaurant.longitude), (location_customer.latitude, location_customer.longitude)).kilometers
                            total_distance = first_distance + second_distance
                            third_distance = geodesic((location_customer.latitude, location_customer.longitude), (nearest_station2.latitude, nearest_station2.longitude)).kilometers
                            total_batteryused = (total_distance + third_distance) * 0.5
                            if drone2.battery_level > total_batteryused:
                                drone2.battery_level -= total_batteryused
                                drone2.save()
                            else:
                                # In reality we will wait them to charge the drone
                                drone2.battery_level = 100
                                drone2.save()
                            flighpath = FlightPath.objects.create(start_location = address_restaurant,end_location = address_customer,drone = drone2,battery_usage = total_batteryused)
                            flighpath.save()
                            # end drone
                            order_general_status = None
                            if (order_general_object.status == 'New order') or (order_general_object.status == 'Preparing'):
                                # Geocode the customer and restaurant addresses
                                # Create the map and add the markers
                                m = folium.Map(location=[location_restaurant.latitude, location_restaurant.longitude], zoom_start=14)
                                print("*"*80)
                                print(nearest_station.latitude, nearest_station.longitude)
                                folium.Marker([nearest_station.latitude, nearest_station.longitude], popup='Charging Station').add_to(m)
                                folium.Marker([nearest_station2.latitude, nearest_station2.longitude], popup='Charging Station2').add_to(m)
                                folium.Marker([location_restaurant.latitude, location_restaurant.longitude], popup='Restaurant').add_to(m)
                                folium.Marker([location_customer.latitude, location_customer.longitude], popup='Customer').add_to(m)
                                # Calculate the route and add it to the map
                                client = openrouteservice.Client(key='5b3ce3597851110001cf62481f738855150c49b3b8e6addabb1c3f67')
                                coords1 = ((nearest_station.longitude, nearest_station.latitude), (location_restaurant.longitude, location_restaurant.latitude))
                                route = client.directions(coordinates=coords1, profile='foot-hiking', format='geojson')
                                coords2 = ((nearest_station2.longitude, nearest_station2.latitude), (location_restaurant.longitude, location_restaurant.latitude))
                                route = client.directions(coordinates=coords2, profile='foot-hiking', format='geojson')
                                folium.plugins.AntPath(locations=[(coord[1], coord[0]) for coord in route['features'][0]['geometry']['coordinates']]).add_to(m)
                                m = m._repr_html_()
                                if order_general_object.status == 'New order':
                                    order_general_status = 'New order'
                                    return render(request,"Delivery.html",{'id':id, 'map': m,'order_general_status':order_general_status,'order_general_id':order_general_id,'total_weight':total_weight,"numberdrone_status":numberdrone_status,"number_drone":number_drone})
                                elif order_general_object.status == 'Preparing':
                                    order_general_status = 'Preparing'
                                    return render(request,"Delivery.html",{'id':id, 'map': m,'order_general_status':order_general_status,'order_general_id':order_general_id,'total_weight':total_weight,"numberdrone_status":numberdrone_status,"number_drone":number_drone})
                                elif order_general_object.status == "Delivering":
                                    order_general_status = 'Delivering'
                                    return render(request,"Delivery.html",{'id':id, 'map': m,'order_general_status':order_general_status,'order_general_id':order_general_id,'total_weight':total_weight,"numberdrone_status":numberdrone_status,"number_drone":number_drone})
                            else:
                                # Create the map and add the markers
                                m = folium.Map(location=[nearest_station.latitude, nearest_station.longitude], zoom_start=14)
                                folium.Marker([location_customer.latitude, location_customer.longitude], popup='Customer').add_to(m)
                                folium.Marker([nearest_station.latitude, nearest_station.longitude], popup='Charging Station').add_to(m)
                                folium.Marker([location_restaurant.latitude, location_restaurant.longitude], popup='Restaurant').add_to(m)
                                # Calculate the route and add it to the map
                                client = openrouteservice.Client(key='5b3ce3597851110001cf62481f738855150c49b3b8e6addabb1c3f67')
                                coords = ((location_customer.longitude, location_customer.latitude), (location_restaurant.longitude, location_restaurant.latitude))
                                route = client.directions(coordinates=coords, profile='foot-hiking', format='geojson')
                                folium.plugins.AntPath(locations=[(coord[1], coord[0]) for coord in route['features'][0]['geometry']['coordinates']]).add_to(m)
                                m = m._repr_html_() 
                                if order_general_object.status == "Ready":
                                    order_general_status = 'Ready'
                                    return render(request,"Delivery.html",{'id':id, 'map': m,'order_general_status':order_general_status,"order_general_id":order_general_id,'total_weight':total_weight,"numberdrone_status":numberdrone_status,"number_drone":number_drone})
                                elif order_general_object.status == "Delivering":
                                    order_general_status = 'Delivering'
                                    return render(request,"Delivery.html",{'id':id, 'map': m,'order_general_status':order_general_status,"order_general_id":order_general_id,'total_weight':total_weight,"numberdrone_status":numberdrone_status,"number_drone":number_drone})
                                else:
                                    order_general_status = 'Delivered'
                                    # drone 1
                                    chargingstations = ChargingStation.objects.all()
                                    min_distance = float('inf')
                                    nearest_station = None
                                    for chargingstation in chargingstations:
                                        numberdrone = ChargingStationStatus.objects.filter(station=chargingstation,status = True).count()
                                        if numberdrone < 10:
                                            # Geocode the charging station location
                                            location_charging = geolocator.geocode(chargingstation.location)
                                            # Calculate the distance to the restaurant
                                            distance = geodesic((location_charging.latitude, location_charging.longitude), (location_customer.latitude, location_customer.longitude)).kilometers
                                            if distance < min_distance:
                                                min_distance = distance
                                                nearest_station = chargingstation
                                    chargingstationstatus = ChargingStationStatus.objects.create(drone=drone,station=nearest_station,status=True)
                                    chargingstationstatus.save()
                                    flighpath = FlightPath.objects.create(start_location = address_customer,end_location = nearest_station.location,drone = drone,battery_usage = third_distance*0.5)
                                    flighpath.save()
                                    drone.battery_level = 100
                                    drone.save()  
                                    # drone 2
                                    chargingstations = ChargingStation.objects.all()
                                    min_distance = float('inf')
                                    nearest_station = None
                                    for chargingstation in chargingstations:
                                        numberdrone = ChargingStationStatus.objects.filter(station=chargingstation,status = True).count()
                                        if numberdrone < 10:
                                            # Geocode the charging station location
                                            location_charging = geolocator.geocode(chargingstation.location)
                                            # Calculate the distance to the restaurant
                                            distance = geodesic((location_charging.latitude, location_charging.longitude), (location_customer.latitude, location_customer.longitude)).kilometers
                                            if distance < min_distance:
                                                min_distance = distance
                                                nearest_station = chargingstation
                                    chargingstationstatus = ChargingStationStatus.objects.create(drone=drone2,station=nearest_station,status=True)
                                    chargingstationstatus.save()
                                    flighpath = FlightPath.objects.create(start_location = address_customer,end_location = nearest_station.location,drone = drone2,battery_usage = third_distance*0.5)
                                    flighpath.save()
                                    drone2.battery_level = 100
                                    drone2.save()                  
                                    return render(request,"Delivery.html",{'id':id, 'map': m,'order_general_status':order_general_status,'order_general_id':order_general_id,'total_weight':total_weight,"numberdrone_status":numberdrone_status,"number_drone":number_drone})
        else:
            numberdrone_status = False
            m = folium.Map(location=[-37.8136, 144.9631], zoom_start=14)
            return render(request,"Delivery.html",{'id':id, 'map': m,'order_general_id':order_general_id,"numberdrone_status":numberdrone_status})
    else:
         m = folium.Map(location=[-37.8136, 144.9631], zoom_start=14)
         return render(request,"Delivery.html",{'id':id, 'map': m})
def MyAddresses(request,id):
    deliveries = Customer_delivery.objects.filter(customer=id)
    customers = Customer.objects.filter(customer_id=id).first()
    return render(request,"My-address.html",{'id':id,'customers':customers,'deliveries':deliveries})
def Favourites(request,id):
    return render(request,"Favourite.html",{'id':id})
def OrderHistory(request,id):
    return render(request,"My-order-history.html",{'id':id})
def Notifications(request,id):
    return render(request,"Notification.html",{'id':id})
def Payment(request,id):
    payments = Paymentmethod.objects.filter(customer_id=id)
    return render(request,"Payment.html",{'id':id,'payments':payments})
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
    restaurant_ordernumbers = Restaurant_Order.objects.filter(restaurant=id)
    number_new_orders=0
    number_preparing_orders = 0 
    number_ready_orders = 0
    number_delivering_orders = 0
    number_delivered_orders = 0
    for restaurant_ordernumber in restaurant_ordernumbers:
        new_orders = Order_General.objects.filter(status='New order',order_id=restaurant_ordernumber.order.order_id).count()
        preparing_orders = Order_General.objects.filter(status='Preparing',order_id=restaurant_ordernumber.order.order_id).count()
        ready_orders = Order_General.objects.filter(status='Ready',order_id=restaurant_ordernumber.order.order_id).count()
        delivering_orders = Order_General.objects.filter(status='Delivering',order_id=restaurant_ordernumber.order.order_id).count()
        delivered_orders = Order_General.objects.filter(status='Delivered',order_id=restaurant_ordernumber.order.order_id).count()
        number_new_orders += new_orders
        number_preparing_orders += preparing_orders
        number_ready_orders += ready_orders
        number_delivering_orders += delivering_orders
        number_delivered_orders += delivered_orders
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
    restaurant_orders = Restaurant_Order.objects.filter(restaurant=id,status="New order")
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
        number_of_orders = len(results)
        number_of_neworders = 0
    restaurant_ordernumbers = Restaurant_Order.objects.filter(restaurant=id)
    number_new_orders=0
    number_preparing_orders = 0 
    number_ready_orders = 0
    number_delivering_orders = 0
    number_delivered_orders = 0
    for restaurant_ordernumber in restaurant_ordernumbers:
        new_orders = Order_General.objects.filter(status='New order',order_id=restaurant_ordernumber.order.order_id).count()
        preparing_orders = Order_General.objects.filter(status='Preparing',order_id=restaurant_ordernumber.order.order_id).count()
        ready_orders = Order_General.objects.filter(status='Ready',order_id=restaurant_ordernumber.order.order_id).count()
        delivering_orders = Order_General.objects.filter(status='Delivering',order_id=restaurant_ordernumber.order.order_id).count()
        delivered_orders = Order_General.objects.filter(status='Delivered',order_id=restaurant_ordernumber.order.order_id).count()
        number_new_orders += new_orders
        number_preparing_orders += preparing_orders
        number_ready_orders += ready_orders
        number_delivering_orders += delivering_orders
        number_delivered_orders += delivered_orders
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
    restaurant_orders = Restaurant_Order.objects.filter(restaurant=id)
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
    restaurant_ordernumbers = Restaurant_Order.objects.filter(restaurant=id)
    number_new_orders=0
    number_preparing_orders = 0 
    number_ready_orders = 0
    number_delivering_orders = 0
    number_delivered_orders = 0
    for restaurant_ordernumber in restaurant_ordernumbers:
        new_orders = Order_General.objects.filter(status='New order',order_id=restaurant_ordernumber.order.order_id).count()
        preparing_orders = Order_General.objects.filter(status='Preparing',order_id=restaurant_ordernumber.order.order_id).count()
        ready_orders = Order_General.objects.filter(status='Ready',order_id=restaurant_ordernumber.order.order_id).count()
        delivering_orders = Order_General.objects.filter(status='Delivering',order_id=restaurant_ordernumber.order.order_id).count()
        delivered_orders = Order_General.objects.filter(status='Delivered',order_id=restaurant_ordernumber.order.order_id).count()
        number_new_orders += new_orders
        number_preparing_orders += preparing_orders
        number_ready_orders += ready_orders
        number_delivering_orders += delivering_orders
        number_delivered_orders += delivered_orders
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
    restaurant_ordernumbers = Restaurant_Order.objects.filter(restaurant=id)
    number_new_orders=0
    number_preparing_orders = 0 
    number_ready_orders = 0
    number_delivering_orders = 0
    number_delivered_orders = 0
    for restaurant_ordernumber in restaurant_ordernumbers:
        new_orders = Order_General.objects.filter(status='New order',order_id=restaurant_ordernumber.order.order_id).count()
        preparing_orders = Order_General.objects.filter(status='Preparing',order_id=restaurant_ordernumber.order.order_id).count()
        ready_orders = Order_General.objects.filter(status='Ready',order_id=restaurant_ordernumber.order.order_id).count()
        delivering_orders = Order_General.objects.filter(status='Delivering',order_id=restaurant_ordernumber.order.order_id).count()
        delivered_orders = Order_General.objects.filter(status='Delivered',order_id=restaurant_ordernumber.order.order_id).count()
        number_new_orders += new_orders
        number_preparing_orders += preparing_orders
        number_ready_orders += ready_orders
        number_delivering_orders += delivering_orders
        number_delivered_orders += delivered_orders
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
    restaurant_ordernumbers = Restaurant_Order.objects.filter(restaurant=id)
    number_new_orders=0
    number_preparing_orders = 0 
    number_ready_orders = 0
    number_delivering_orders = 0
    number_delivered_orders = 0
    for restaurant_ordernumber in restaurant_ordernumbers:
        new_orders = Order_General.objects.filter(status='New order',order_id=restaurant_ordernumber.order.order_id).count()
        preparing_orders = Order_General.objects.filter(status='Preparing',order_id=restaurant_ordernumber.order.order_id).count()
        ready_orders = Order_General.objects.filter(status='Ready',order_id=restaurant_ordernumber.order.order_id).count()
        delivering_orders = Order_General.objects.filter(status='Delivering',order_id=restaurant_ordernumber.order.order_id).count()
        delivered_orders = Order_General.objects.filter(status='Delivered',order_id=restaurant_ordernumber.order.order_id).count()
        number_new_orders += new_orders
        number_preparing_orders += preparing_orders
        number_ready_orders += ready_orders
        number_delivering_orders += delivering_orders
        number_delivered_orders += delivered_orders
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
    restaurant_orders = Restaurant_Order.objects.filter(restaurant=id)
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
    restaurant_ordernumbers = Restaurant_Order.objects.filter(restaurant=id)
    number_new_orders=0
    number_preparing_orders = 0 
    number_ready_orders = 0
    number_delivering_orders = 0
    number_delivered_orders = 0
    for restaurant_ordernumber in restaurant_ordernumbers:
        new_orders = Order_General.objects.filter(status='New order',order_id=restaurant_ordernumber.order.order_id).count()
        preparing_orders = Order_General.objects.filter(status='Preparing',order_id=restaurant_ordernumber.order.order_id).count()
        ready_orders = Order_General.objects.filter(status='Ready',order_id=restaurant_ordernumber.order.order_id).count()
        delivering_orders = Order_General.objects.filter(status='Delivering',order_id=restaurant_ordernumber.order.order_id).count()
        delivered_orders = Order_General.objects.filter(status='Delivered',order_id=restaurant_ordernumber.order.order_id).count()
        number_new_orders += new_orders
        number_preparing_orders += preparing_orders
        number_ready_orders += ready_orders
        number_delivering_orders += delivering_orders
        number_delivered_orders += delivered_orders
    number = {
        'number_new_orders': number_new_orders,
        'number_preparing_orders': number_preparing_orders,
        'number_ready_orders': number_ready_orders,
        'number_delivering_orders': number_delivering_orders,
        'number_delivered_orders': number_delivered_orders
    }

    return render(request, 'Res-order-tracking.html', {'id': id, 'number': number, 'order_tracking': order_tracking})