from rest_framework import serializers
from .models import Booking, Package, BusinessHours, Address

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
                  'confirmed', 'created_at', 'address')
        read_only_fields = ('confirmed', 'created_at')

    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        
        if address_data:
            address = Address.objects.create(**address_data)
            validated_data['address'] = address
        
        booking = Booking.objects.create(**validated_data)
        return booking
    
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        
        if address_data:
            address = instance.address
            if address:
                # Update existing address
                for key, value in address_data.items():
                    setattr(address, key, value)
                address.save()
            else:
                # Create new address
                address = Address.objects.create(**address_data)
                instance.address = address
        
        # Update other booking fields
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        instance.save()
        return instance
    
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
    
class GuestBookingLookupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        # Check if bookings exist for this email
        if not Booking.objects.filter(email=value).exists():
            raise serializers.ValidationError("No bookings found for this email address")
        return value

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'street_address', 'city', 'state', 'zip_code')