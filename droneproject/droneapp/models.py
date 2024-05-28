from django.db import models

# Add the missing import statement for DecimalField
from django.db.models import DecimalField

class Admin(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
class ChargingStation(models.Model):
    station_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField(default=10)
class Drone(models.Model):
    drone_id = models.AutoField(primary_key=True)
    battery_level = models.IntegerField(default=100)

class FlightPath(models.Model):
    path_id = models.AutoField(primary_key=True)
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    battery_usage = models.IntegerField()
    drone = models.ForeignKey(Drone, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=True)


class ChargingStationStatus(models.Model):
    checking_station_id = models.AutoField(primary_key=True)
    drone = models.ForeignKey(Drone, on_delete=models.DO_NOTHING)
    station = models.ForeignKey(ChargingStation, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=True)
class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, default="1234567890")
    email = models.EmailField(default="abc@gmail.com")
    password = models.CharField(max_length=255, default="123456")
    menu_items = models.CharField(max_length=255)
    opening_time = models.TimeField(default='00:00:00')
    closing_time = models.TimeField(default='23:59:59')
    picture_link = models.CharField(max_length=255, default="123")

class Food(models.Model):
    food_id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.DO_NOTHING)
    food_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Fix the missing import for DecimalField
    total_weight = models.DecimalField(max_digits=10, decimal_places=2)  # Fix the missing import for DecimalField
    category = models.CharField(max_length=255)
    picture_link = models.CharField(max_length=255)

class Paymentmethod(models.Model):
    payment_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    card_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    cvc = models.IntegerField()
    expiry_date = models.CharField(max_length=255)

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.DecimalField(max_digits=10, decimal_places=0)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255,default='Melbourne')
    state = models.CharField(max_length=255)
    postcode = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=255)
class Customer_delivery(models.Model):
    delivery_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    delivery_address = models.CharField(max_length=255)
    delivery_city = models.CharField(max_length=255)
    delivery_state = models.CharField(max_length=255)
    delivery_postcode = models.IntegerField()
    delivery_phone = models.CharField(max_length=255)  

class Order_General(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)  
    payment = models.ForeignKey(Paymentmethod, on_delete=models.DO_NOTHING)
    delivery_status = models.CharField(max_length=255, default='Not Finished')
    drone = models.ForeignKey(Drone, on_delete=models.DO_NOTHING,default= 1)
    order_placed = models.BooleanField(default=True)
    order_packed = models.BooleanField(default=False)
    order_shipped = models.BooleanField(default=False)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=5.0)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=5.0)
    total_price = models.IntegerField(default=0)
    time_ordered = models.CharField(max_length=255,default='00:00:00')
    street = models.CharField(max_length=255,default='123 street')
    zip_code = models.IntegerField(default=3000)
    city = models.CharField(max_length=255,default='Melbourne')
    province = models.CharField(max_length=255,default='VIC')
    phone = models.CharField(max_length=255,default='1234567890')
    pickup_time = models.TimeField(default='00:00:00')
    total_quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=255, choices=[
        ('New order', 'New order'),
        ('Preparing', 'Preparing'),
        ('Ready', 'Ready'),
        ('Delivering', 'Delivering'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ], default='New order')

class Order_Food(models.Model):
    order_food = models.AutoField(primary_key=True)
    restaurant= models.ForeignKey(Restaurant, on_delete=models.DO_NOTHING) 
    order_generalid = models.ForeignKey(Order_General, on_delete=models.DO_NOTHING)
    food = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)

class Restaurant_Order(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order_General, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=255, choices=[
        ('New order', 'New order'),
        ('Preparing', 'Preparing'),
        ('Ready', 'Ready'),
        ('Delivering', 'Delivering'),
        ('Delivered', 'Delivered'),
    ], default='New order')

