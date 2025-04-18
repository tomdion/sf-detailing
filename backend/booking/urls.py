from django.urls import path
from booking import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.api_root, name = 'api-root'),
    path('booking-list/', views.BookingListView.as_view(), name ='booking-list'),
    path('booking-list/<int:id>/', views.BookingDeleteView.as_view(), name='booking-delete'),
    path('user-bookings/', views.UserBookingsView.as_view(), name='user-bookings'),
    path('guest-bookings/', views.GuestBookingsView.as_view(), name='guest-bookings'),
    path('confirm/', views.confirm_booking, name='booking-confirm'),
    path('business-hours/', views.BusinessHoursView.as_view(), name='business-hours'),
    path('packages/', views.PackageListView.as_view(), name='packages'),
    path('addons/', views.AddonListView.as_view(), name='addon-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)