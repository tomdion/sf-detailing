from rest_framework import serializers
from .models import Booking

class BookingSerializizer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'date', 'time', 'package', 'vehicle')