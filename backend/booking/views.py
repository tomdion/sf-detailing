from rest_framework import generics, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Booking, Package
from .serializers import BookingSerializer
from datetime import datetime, timedelta
from .services import EmailService

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'bookings': reverse('booking-list', request=request, format=format),
        'user-bookings': reverse('user-bookings', request=request, format=format),
        'booking-confirm': reverse('booking-confirm', request=request, format=format) + '?token={token}'
    })

class BookingListView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_serializer_context(self):
        """Add request to serializer context"""
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        package = serializer.validated_data.get('package')
        time_restriction = self.get_time_restriction(package)

        if self.check_time_conflict(serializer.validated_data['date'], serializer.validated_data['time'], time_restriction):
            raise serializers.ValidationError("A booking already exists within the restricted time.")
        
        # Save the booking
        booking = serializer.save()
        
        # Send confirmation email
        try:
            EmailService.send_booking_confirmation(booking)
        except Exception as e:
            # Log the error but don't prevent booking creation
            print(f"Error sending confirmation email: {e}")

    def get_time_restriction(self, package):
        """Get time restriction in hours based on package"""
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

class UserBookingsView(generics.ListAPIView):
    """View for retrieving a user's booking history"""
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only bookings for the authenticated user"""
        return Booking.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([AllowAny])
def confirm_booking(request):
    """Endpoint to confirm a booking using the confirmation token"""
    token = request.query_params.get('token')
    if not token:
        return Response({"error": "Confirmation token is required"}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    try:
        booking = Booking.objects.get(confirmation_token=token, confirmed=False)
        booking.confirmed = True
        booking.save()
        
        # Send confirmation notification
        try:
            EmailService.send_booking_confirmed(booking)
        except Exception as e:
            print(f"Error sending confirmation notification: {e}")
            
        return Response({"message": "Booking confirmed successfully"}, 
                        status=status.HTTP_200_OK)
    except Booking.DoesNotExist:
        return Response({"error": "Invalid or expired confirmation token"}, 
                        status=status.HTTP_404_NOT_FOUND)
    
class BookingDeleteView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'id'