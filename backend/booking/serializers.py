from rest_framework import serializers
from .models import Booking, Package

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id', 'name', 'display_name', 'price', 'description')

class BookingSerializer(serializers.ModelSerializer):
    # Add a nested serializer for displaying package details in responses
    package_details = PackageSerializer(source='package', read_only=True)
    
    class Meta:
        model = Booking
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 
                  'date', 'time', 'package', 'package_details', 'vehicle',
                  'confirmed', 'created_at')
        read_only_fields = ('confirmed', 'created_at')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
    
    def create(self, validated_data):
        import uuid
        validated_data['confirmation_token'] = str(uuid.uuid4())
        
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
            
        return super().create(validated_data)