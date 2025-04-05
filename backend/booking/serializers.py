from rest_framework import serializers
from .models import Booking, Package, BusinessHours, Address, Addon, BookingAddon, VehiclePackagePrice
import uuid

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'street_address', 'city', 'state', 'zip_code')

class AddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addon
        fields = ('id', 'name', 'display_name', 'price', 'description')

class BookingAddonSerializer(serializers.ModelSerializer):
    addon_details = AddonSerializer(source='addon', read_only=True)
    
    class Meta:
        model = BookingAddon
        fields = ('id', 'addon', 'addon_details', 'quantity', 'price_at_booking')
        read_only_fields = ('id', 'price_at_booking')

class VehiclePackagePriceSerializer(serializers.ModelSerializer):
    vehicle_type_display = serializers.CharField(source='get_vehicle_type_display', read_only=True)
    
    class Meta:
        model = VehiclePackagePrice
        fields = ('id', 'vehicle_type', 'vehicle_type_display', 'price')

class PackageSerializer(serializers.ModelSerializer):
    vehicle_prices = VehiclePackagePriceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Package
        fields = ('id', 'name', 'display_name', 'price', 'description', 'vehicle_prices')

class BusinessHoursSerializer(serializers.ModelSerializer):
    day_name = serializers.SerializerMethodField()
    
    class Meta:
        model = BusinessHours
        fields = ('id', 'day', 'day_name', 'opening_time', 'closing_time', 'is_open')
        
    def get_day_name(self, obj):
        return obj.get_day_display()

class BookingSerializer(serializers.ModelSerializer):
    package_details = PackageSerializer(source='package', read_only=True)
    addons = BookingAddonSerializer(many=True, read_only=True)
    address = AddressSerializer(required=False)
    addon_ids = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    total_price = serializers.SerializerMethodField()
    vehicle_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 
                  'date', 'time', 'package', 'package_details', 'vehicle',
                  'confirmed', 'created_at', 'address', 'addons', 'addon_ids', 
                  'total_price', 'vehicle_price')
        read_only_fields = ('confirmed', 'created_at', 'total_price', 'vehicle_price')

    def get_vehicle_price(self, obj):
        """Get the vehicle-specific price for this package"""
        try:
            price = VehiclePackagePrice.objects.get(
                package=obj.package,
                vehicle_type=obj.vehicle
            ).price
            return float(price)
        except VehiclePackagePrice.DoesNotExist:
            # If no vehicle-specific price exists, fall back to the default package price
            return float(obj.package.price) if obj.package else 0
    
    def get_total_price(self, obj):
        """Calculate total price including add-ons, using vehicle-specific package price"""
        # Get vehicle-specific package price
        package_price = self.get_vehicle_price(obj)
        
        # Add add-on prices
        addon_price = sum(float(ba.get_total()) for ba in obj.addons.all())
        
        return package_price + addon_price
    
    def create(self, validated_data):
        # Extract nested fields
        address_data = validated_data.pop('address', None)
        addon_data = validated_data.pop('addon_ids', [])
        
        # Add confirmation token
        validated_data['confirmation_token'] = str(uuid.uuid4())
        
        # Set user if authenticated
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        
        # Create address if provided
        address = None
        if address_data:
            address = Address.objects.create(**address_data)
            validated_data['address'] = address
        
        # Create booking
        booking = Booking.objects.create(**validated_data)
        
        # Process addons
        for item in addon_data:
            addon_id = item.get('id')
            quantity = item.get('quantity', 1)
            
            try:
                addon = Addon.objects.get(id=addon_id, active=True)
                BookingAddon.objects.create(
                    booking=booking,
                    addon=addon,
                    quantity=quantity
                )
            except Addon.DoesNotExist:
                pass
        
        return booking
    
    def update(self, instance, validated_data):
        # Extract nested fields
        address_data = validated_data.pop('address', None)
        addon_data = validated_data.pop('addon_ids', None)
        
        # Update address if provided
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
        
        # Process addons if provided
        if addon_data is not None:
            # Clear existing addons
            instance.addons.all().delete()
            
            # Add new ones
            for item in addon_data:
                addon_id = item.get('id')
                quantity = item.get('quantity', 1)
                
                try:
                    addon = Addon.objects.get(id=addon_id, active=True)
                    BookingAddon.objects.create(
                        booking=instance,
                        addon=addon,
                        quantity=quantity
                    )
                except Addon.DoesNotExist:
                    pass
        
        return instance
    
    def validate(self, data):
        is_valid, message = BusinessHours.is_valid_booking_time(data['date'], data['time'])
        if not is_valid:
            raise serializers.ValidationError(message)
        
        return data
    
class GuestBookingLookupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        # Check if bookings exist for this email
        if not Booking.objects.filter(email=value).exists():
            raise serializers.ValidationError("No bookings found for this email address")
        return value