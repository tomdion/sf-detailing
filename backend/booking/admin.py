from django.contrib import admin
from .models import Booking, Package, BusinessHours
# Register your models here.
admin.site.register(Booking)

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'price')
    list_editable = ['price']  # Only include the price field
    list_display_links = ['display_name']  # Display name links to the edit form
    search_fields = ('name', 'display_name')

@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ('get_day_display', 'is_open', 'opening_time', 'closing_time')
    list_editable = ['is_open', 'opening_time', 'closing_time']
    
    def get_day_display(self, obj):
        return obj.get_day_display()
    get_day_display.short_description = 'Day'