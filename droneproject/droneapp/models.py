from django.db import models

# Add the missing import statement for DecimalField
from django.db.models import DecimalField

class Drone(models.Model):
    drone_id = models.AutoField(primary_key=True)
    station_id = models.IntegerField(null=True, blank=True)
    battery_level = models.IntegerField(default=100)
    current_load = models.CharField(max_length=255, null=True, blank=True)

class FlightPath(models.Model):
    path_id = models.AutoField(primary_key=True)
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    battery_usage = models.IntegerField()
    drone = models.ForeignKey(Drone, on_delete=models.DO_NOTHING)

class ChargingStation(models.Model):
    station_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField(default=10)

class ChargingStationStatus(models.Model):
    checking_station_id = models.AutoField(primary_key=True)
    drone = models.ForeignKey(Drone, on_delete=models.DO_NOTHING)
    station = models.ForeignKey(ChargingStation, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=True)

class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    menu_items = models.CharField(max_length=255)
    opening_hours = models.CharField(max_length=255)
    picture_link = models.CharField(max_length=255)

class Food(models.Model):
    food_id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.DO_NOTHING)
    food_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Fix the missing import for DecimalField
    total_weight = models.DecimalField(max_digits=10, decimal_places=2)  # Fix the missing import for DecimalField
    category = models.CharField(max_length=255)
    picture_link = models.CharField(max_length=255)

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    card_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=255)
    cvc = models.IntegerField()
    expiry_date = models.CharField(max_length=255)

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    phone = models.DecimalField(max_digits=10, decimal_places=0)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postcode = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=255)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    food = models.ForeignKey(Food, on_delete=models.DO_NOTHING)
    payment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING)
    delivery_status = models.CharField(max_length=255)
    drone = models.ForeignKey(Drone, on_delete=models.DO_NOTHING)
    order_placed = models.BooleanField(default=True)
    order_packed = models.BooleanField(default=False)
    order_shipped = models.BooleanField(default=False)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=5.0)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=5.0)