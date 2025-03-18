from django.utils import timezone
from django.db import models
from django.conf import settings
from datetime import datetime

class Package(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.display_name} (${self.price})"
    
    class Meta:
        ordering = ['price']

class BusinessHours(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday')
    ]
    
    day = models.IntegerField(choices=DAYS_OF_WEEK, unique=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_open = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['day']
        verbose_name = 'Business Hours'
        verbose_name_plural = 'Business Hours'
    
    def __str__(self):
        day_name = dict(self.DAYS_OF_WEEK)[self.day]
        if self.is_open:
            return f"{day_name}: {self.opening_time.strftime('%I:%M %p')} - {self.closing_time.strftime('%I:%M %p')}"
        return f"{day_name}: Closed"
    
    @classmethod
    def is_within_operating_hours(cls, booking_date, booking_time):
        """Check if the given date and time falls within operating hours"""
        day_of_week = booking_date.weekday()
        
        try:
            hours = cls.objects.get(day=day_of_week)
            
            # If business is closed on this day, reject the booking
            if not hours.is_open:
                return False, "We are closed on this day."
            
            # Check if time is within operating hours
            if hours.opening_time <= booking_time <= hours.closing_time:
                return True, ""
            else:
                return False, f"Our hours on this day are {hours.opening_time.strftime('%I:%M %p')} to {hours.closing_time.strftime('%I:%M %p')}."
        
        except cls.DoesNotExist:
            # If no hours defined for this day, assume closed
            return False, "No operating hours defined for this day."
    
    @classmethod
    def is_valid_booking_time(cls, booking_date, booking_time):
        """Check if the booking date and time are valid (in future and within hours)"""
        now = timezone.now()
        booking_datetime = datetime.combine(booking_date, booking_time)
        booking_datetime = timezone.make_aware(booking_datetime)
        
        if booking_datetime <= now:
            return False, "Cannot book for dates or times in the past."
        
        return cls.is_within_operating_hours(booking_date, booking_time)

class Booking(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=250)
    phone_number = models.CharField(max_length=25)
    date = models.DateField()
    time = models.TimeField()
    package = models.ForeignKey(Package, on_delete=models.PROTECT)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = 'bookings'
    )

    confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    VEHICLE_TYPE = [
        ('car', 'Car'),
        ('suv', 'SUV'),
        ('truck', 'Truck'),
    ]
    vehicle = models.CharField(max_length=20, choices=VEHICLE_TYPE)

    def __str__(self):
        full_time = f"{self.date.strftime('%Y/%m/%d')} at {self.time.strftime('%I:%M %p')}"
        return f"Booking by {self.last_name} on {full_time}"
    
    class Meta:
        ordering = ['-date', '-time']