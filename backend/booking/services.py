from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class EmailService:
    @staticmethod
    def send_booking_confirmation(booking):
        """
        Send a booking confirmation email to the customer
        """
        confirmation_url = f"{settings.FRONTEND_URL}/confirm-booking/{booking.confirmation_token}"
        
        # Prepare email context
        context = {
            'booking': booking,
            'confirmation_url': confirmation_url,
            'is_user': booking.user is not None
        }
        
        # Render email content from templates
        html_message = render_to_string('booking/email/booking_confirmation.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject='Confirm Your Booking',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_booking_confirmed(booking):
        """
        Send a notification that the booking has been confirmed
        """
        # Prepare email context
        context = {
            'booking': booking,
            'is_user': booking.user is not None
        }
        
        # Render email content from templates
        html_message = render_to_string('booking/email/booking_confirmed.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject='Your Booking is Confirmed',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email],
            html_message=html_message,
            fail_silently=False,
        )