# Generated by Django 5.0.4 on 2024-05-17 04:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("droneapp", "0012_rename_quatity_order_food_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order_food",
            name="restaurant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="droneapp.restaurant"
            ),
        ),
    ]
