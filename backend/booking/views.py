from rest_framework import generics, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Booking, Package
from .serializers import BookingSerializizer
from datetime import datetime, timedelta
# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'bookings':reverse('booking-list', request=request, format=format)
    })

class BookingListView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializizer

    def perform_create(self, serializer):
        package = serializer.validated_data.get('package')
        time_restriction = self.get_time_restriction(package)

        if self.check_time_conflict(serializer.validated_data['date'], serializer.validated_data['time'], time_restriction):
            raise serializers.ValidationError("A booking already exists within the restricted time.")
        
        serializer.save()

    def get_time_restriction(self, package):
        """Get time restriction in hours based on package"""
        # Now expecting a Package model instance instead of a string
        try:
            package_name = package.name
            if package_name == 'interior':
                return 3
            elif package_name == 'exterior':
                return 1
            elif package_name == 'interior_exterior':
                return 3.5
            return 0
        except AttributeError:
            # Handle case where package is not a Package instance
            return 0
    
    def check_time_conflict(self, booking_date, booking_time, restriction_hours):
        booking_datetime = datetime.combine(booking_date, booking_time)
        start_time = booking_datetime - timedelta(hours=restriction_hours)
        end_time = booking_datetime + timedelta(hours=restriction_hours)
        
        # Extract just the time component for comparison
        start_time_only = start_time.time()
        end_time_only = end_time.time()
        
        conflicting_bookings = Booking.objects.filter(date=booking_date)
        
        for booking in conflicting_bookings:
            booking_time = booking.time
            if start_time_only <= booking_time <= end_time_only:
                return True
                
        return False
    
class BookingDeleteView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializizer
    lookup_field = 'id'