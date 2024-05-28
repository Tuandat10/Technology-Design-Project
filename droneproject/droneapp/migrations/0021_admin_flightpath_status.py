# Generated by Django 5.0.4 on 2024-05-27 17:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("droneapp", "0020_order_food_price"),
    ]

    operations = [
        migrations.CreateModel(
            name="Admin",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=255)),
                ("password", models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name="flightpath",
            name="status",
            field=models.BooleanField(default=True),
        ),
    ]
