# Generated by Django 5.1.7 on 2025-03-25 02:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0012_address_alter_booking_package_booking_address"),
    ]

    operations = [
        migrations.CreateModel(
            name="Addon",
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
                ("name", models.CharField(max_length=50, unique=True)),
                ("display_name", models.CharField(max_length=100)),
                ("price", models.DecimalField(decimal_places=2, max_digits=6)),
                ("description", models.TextField(blank=True)),
                ("active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["price"],
            },
        ),
        migrations.CreateModel(
            name="BookingAddon",
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
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "price_at_booking",
                    models.DecimalField(decimal_places=2, max_digits=6),
                ),
                (
                    "addon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="booking.addon"
                    ),
                ),
                (
                    "booking",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="addons",
                        to="booking.booking",
                    ),
                ),
            ],
            options={
                "unique_together": {("booking", "addon")},
            },
        ),
    ]
