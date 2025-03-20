from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of a booking or admins to delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow admin users to delete any booking
        if request.user and request.user.is_staff:
            return True
        
        # Allow users to delete their own bookings
        if request.user and request.user.is_authenticated:
            return obj.user == request.user
        
        # Allow guests to delete bookings they created (by matching email)
        if obj.user is None and hasattr(request, 'session'):
            # Check if the booking's email is stored in the session
            booking_email = request.session.get('booking_email')
            if booking_email and booking_email == obj.email:
                return True
        
        return False