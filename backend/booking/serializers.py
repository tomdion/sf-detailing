from rest_framework import serializers
from .models import Booking, Package

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id', 'name', 'display_name', 'price', 'description')

class BookingSerializizer(serializers.ModelSerializer):
    # Add a nested serializer for displaying package details in responses
    package_details = PackageSerializer(source='package', read_only=True)
    
    class Meta:
        model = Booking
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 
                  'date', 'time', 'package', 'package_details', 'vehicle')
        
    def to_representation(self, instance):
        """Override to include nested package details in the response"""
        representation = super().to_representation(instance)
        return representation