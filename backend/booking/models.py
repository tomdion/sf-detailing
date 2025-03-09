from django.db import models

class Package(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.display_name} (${self.price})"
    
    class Meta:
        ordering = ['price']

class Booking(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=250)
    phone_number = models.CharField(max_length=25)
    date = models.DateField()
    time = models.TimeField()

    # New ForeignKey field (replace the old CharField)
    package = models.ForeignKey(Package, on_delete=models.PROTECT)

    VEHICLE_TYPE = [
        ('car', 'Car'),
        ('suv', 'SUV'),
        ('truck', 'Truck'),
    ]
    vehicle = models.CharField(max_length=20, choices=VEHICLE_TYPE)

    def __str__(self):
        full_time = f"{self.date.strftime('%Y/%m/%d')} at {self.time.strftime('%I:%M %p')}"
        return f"Booking by {self.last_name} on {full_time}"