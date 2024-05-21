from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Drone)
admin.site.register(FlightPath)
admin.site.register(ChargingStation)
admin.site.register(ChargingStationStatus)
admin.site.register(Restaurant)
admin.site.register(Food)
admin.site.register(Paymentmethod)
admin.site.register(Customer)
admin.site.register(Order_General)
admin.site.register(Customer_delivery)
admin.site.register(Order_Food)
admin.site.register(Restaurant_Order)