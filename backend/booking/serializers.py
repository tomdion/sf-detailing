from rest_framework import serializers
from .models import Booking, Package, BusinessHours

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id', 'name', 'display_name', 'price', 'description')

class BusinessHoursSerializer(serializers.ModelSerializer):
    day_name = serializers.SerializerMethodField()
    
    class Meta:
        model = BusinessHours
        fields = ('id', 'day', 'day_name', 'opening_time', 'closing_time', 'is_open')
        
    def get_day_name(self, obj):
        return obj.get_day_display()

class BookingSerializer(serializers.ModelSerializer):
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
    
    def validate(self, data):
        is_valid, message = BusinessHours.is_valid_booking_time(data['date'], data['time'])
        if not is_valid:
            raise serializers.ValidationError(message)
        
        return data
    
    def create(self, validated_data):
        import uuid
        validated_data['confirmation_token'] = str(uuid.uuid4())
        
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
            
        return super().create(validated_data)