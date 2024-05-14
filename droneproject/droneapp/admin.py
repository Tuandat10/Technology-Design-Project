from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Drone)
admin.site.register(FlightPath)
admin.site.register(ChargingStation)
admin.site.register(ChargingStationStatus)
admin.site.register(Restaurant)
admin.site.register(Food)
admin.site.register(Payment)
admin.site.register(Customer)
admin.site.register(Order)
