# Generated by Django 5.0.4 on 2024-05-13 06:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("droneapp", "0002_alter_food_price_alter_food_total_weight_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ChargingStations",
            new_name="ChargingStation",
        ),
        migrations.RenameModel(
            old_name="Customers",
            new_name="Customer",
        ),
        migrations.RenameModel(
            old_name="FlightPaths",
            new_name="FlightPath",
        ),
        migrations.RenameModel(
            old_name="Orders",
            new_name="Order",
        ),
        migrations.RenameModel(
            old_name="Restaurants",
            new_name="Restaurant",
        ),
    ]
