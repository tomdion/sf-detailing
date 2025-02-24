from django.db import models

# Create your models here.
class Booking(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=250)
    phone_number = models.CharField(max_length=25)
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

    def __str__(self):
        full_time = f"{self.date.strftime('%Y/%m/%d')} at {self.time.strftime('%I:%M %p')}"
        return f"Booking by {self.last_name} on {full_time}"