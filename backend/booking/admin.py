# backend/booking/admin.py (updated)

from django.contrib import admin
from .models import Booking, Package, BusinessHours, Addon, BookingAddon, VehiclePackagePrice

# Register your models here.
admin.site.register(Booking)

class VehiclePriceInline(admin.TabularInline):
    model = VehiclePackagePrice
    extra = 3  # Show 3 empty forms
    min_num = 3  # Require at least 3 (one for each vehicle type)

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'price')
    list_editable = ['price']
    search_fields = ('name', 'display_name')
    inlines = [VehiclePriceInline]

@admin.register(VehiclePackagePrice)
class VehiclePackagePriceAdmin(admin.ModelAdmin):
    list_display = ('package', 'vehicle_type', 'price')
    list_editable = ['price']
    list_filter = ('package', 'vehicle_type')

@admin.register(Addon)
class AddonAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'price', 'active')
    list_editable = ['price', 'active']
    search_fields = ['name', 'display_name', 'description']
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, f'Activated {updated} add-ons.')
    make_active.short_description = "Mark selected add-ons as active"
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, f'Deactivated {updated} add-ons.')
    make_inactive.short_description = "Mark selected add-ons as inactive"

class BookingAddonInline(admin.TabularInline):
    model = BookingAddon
    extra = 0

@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ('get_day_display', 'is_open', 'opening_time', 'closing_time')
    list_editable = ['is_open', 'opening_time', 'closing_time']
    
    def get_day_display(self, obj):
        return obj.get_day_display()
    get_day_display.short_description = 'Day'