from rest_framework import generics, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from .models import Booking, Package, BusinessHours
from .serializers import BookingSerializer, BusinessHoursSerializer, GuestBookingLookupSerializer
from .services import EmailService
from .permissions import IsAdminUser, IsOwnerOrAdmin

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'bookings': reverse('booking-list', request=request, format=format),
        'user-bookings': reverse('user-bookings', request=request, format=format),
        'guest-bookings': reverse('guest-bookings', request=request, format=format),
        'booking-confirm': reverse('booking-confirm', request=request, format=format) + '?token={token}',
        'business-hours': reverse('business-hours', request=request, format=format)
    })

class BusinessHoursView(generics.ListAPIView):
    """View for retrieving business hours"""
    queryset = BusinessHours.objects.all()
    serializer_class = BusinessHoursSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

class BookingListView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    
    def get_permissions(self):
        """
        Return different permissions depending on the HTTP method:
        - GET: Admin users only
        - POST: Anyone can create a booking
        """
        if self.request.method == 'GET':
            return [IsAdminUser()]
        return [AllowAny()]
    
    def get_queryset(self):
        """Return all bookings, but only for admin users"""
        return Booking.objects.all()

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
        
        booking = serializer.save()
        
        # Store the email in session for guest users to manage their bookings
        if not self.request.user.is_authenticated:
            email = serializer.validated_data.get('email')
            self.request.session['booking_email'] = email
        
        try:
            EmailService.send_booking_confirmation(booking)
        except Exception as e:
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
        booking_datetime = timezone.datetime.combine(booking_date, booking_time)
        start_time = booking_datetime - timedelta(hours=restriction_hours)
        end_time = booking_datetime + timedelta(hours=restriction_hours)
        
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

class GuestBookingsView(APIView):
    """View for guests to retrieve their bookings by email"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = GuestBookingLookupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # Store email in session for later use in deletion
            request.session['booking_email'] = email
            
            bookings = Booking.objects.filter(email=email)
            booking_serializer = BookingSerializer(bookings, many=True)
            
            return Response(booking_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    permission_classes = [IsOwnerOrAdmin]
    
    def get_serializer_context(self):
        """Add request to serializer context"""
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def perform_destroy(self, instance):
        booking_datetime = timezone.make_aware(
            timezone.datetime.combine(instance.date, instance.time)
        )
        now = timezone.now()
        
        if (booking_datetime - now).total_seconds() < 24 * 3600:
            raise serializers.ValidationError("Bookings must be cancelled at least 24 hours in advance.")
        
        super().perform_destroy(instance)