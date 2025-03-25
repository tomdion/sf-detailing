from rest_framework import serializers
from .models import Booking, Package, BusinessHours, Address, Addon, BookingAddon

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
    addons = BookingAddonSerializer(many=True, read_only=True)
    addon_ids = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    total_price = serializers.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        read_only=True, 
        source='total_price'
    )
    
    class Meta:
        model = Booking
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 
                  'date', 'time', 'package', 'package_details', 'vehicle',
                  'confirmed', 'created_at', 'address', 'addons', 'addon_ids', 'total_price')
        read_only_fields = ('confirmed', 'created_at')

    def create(self, validated_data):
        addon_data = validated_data.pop('addon_ids', [])
        booking = super().create(validated_data)
        
        # Process addons
        self._process_addons(booking, addon_data)
        
        return booking
    
    def update(self, instance, validated_data):
        addon_data = validated_data.pop('addon_ids', None)
        booking = super().update(instance, validated_data)
        
        # Process addons only if they were included in the request
        if addon_data is not None:
            # Clear existing addons
            instance.addons.all().delete()
            # Add new ones
            self._process_addons(booking, addon_data)
        
        return booking
    
    def _process_addons(self, booking, addon_data):
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
                # Silently ignore invalid add-ons or log them
                pass

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