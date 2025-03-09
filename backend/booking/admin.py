from django.contrib import admin
from .models import Booking, Package
# Register your models here.
admin.site.register(Booking)

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'price')
    list_editable = ['price']  # Only include the price field
    list_display_links = ['display_name']  # Display name links to the edit form
    search_fields = ('name', 'display_name')