from django.db import models

# Create your models here.
class Booking(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=250)
    phone_number = models.CharField(max_length=25)
    people = models.PositiveIntegerField(default=1)
    date = models.DateField()
    time = models.TimeField()

    PACKAGE_TYPE = [
        ('interior', 'Interior'),
        ('exterior', 'Exterior'),
        ('interior + exterior', 'Interior + Exterior'),
    ]

    package = models.CharField(max_length=20, choices=PACKAGE_TYPE)

    VEHICLE_TYPE = [
        ('car', 'Car'),
        ('suv', 'SUV'),
        ('truck', 'Truck'),
    ]

    vehicle = models.CharField(max_length=20, choices=VEHICLE_TYPE)

