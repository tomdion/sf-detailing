from rest_framework import generics, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Booking
from .serializers import BookingSerializizer
from datetime import datetime, timedelta
# Create your views here.

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'bookings':reverse('booking-list', request=request, format=format)
    })

class BookingListView(generics.ListCreateAPIView):
    queryset =  Booking.objects.all()
    serializer_class = BookingSerializizer

    def perform_create(self, serializer):
        booking_type = serializer.validated_data.get('package')
        print(booking_type)
        time_restriction = self.get_time_restriction(booking_type)

        if self.check_time_conflict(serializer.validated_data['date'], serializer.validated_data['time'], time_restriction):
            raise serializers.ValidationError("A booking already exists within the restricted time.")
        
        serializer.save()

    def get_time_restriction(self, package_type):
        if package_type == 'interior':
            return 3
        elif package_type == 'exterior':
            return 1
        elif package_type == 'interior + exterior':
            return 3.5
        return 0
    
    def check_time_conflict(self, booking_date, booking_time, restriction_hours):
        booking_datetime = datetime.combine(booking_date, booking_time)
        conflicting_bookings = Booking.objects.filter(
            date = booking_date,
            time__gte = (booking_datetime - timedelta(hours=restriction_hours)),
            time__lte = (booking_datetime + timedelta(hours=restriction_hours))
        )
        return conflicting_bookings.exists()
    
class BookingDeleteView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializizer
    lookup_field = 'id'