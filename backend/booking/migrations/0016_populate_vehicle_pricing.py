# Generated manually

from django.db import migrations

def populate_vehicle_pricing(apps, schema_editor):
    Package = apps.get_model('booking', 'Package')
    VehiclePackagePrice = apps.get_model('booking', 'VehiclePackagePrice')
    
    # Define the pricing matrix
    pricing_data = {
        'interior': {
            'car': 50.00,
            'suv': 70.00,
            'truck': 90.00
        },
        'exterior': {
            'car': 60.00,
            'suv': 80.00,
            'truck': 100.00
        },
        'interior_exterior': {
            'car': 100.00,
            'suv': 120.00,
            'truck': 160.00
        }
    }
    
    # Create vehicle-specific pricing for each package
    for package_name, prices in pricing_data.items():
        try:
            package = Package.objects.get(name=package_name)
            
            for vehicle_type, price in prices.items():
                VehiclePackagePrice.objects.create(
                    package=package,
                    vehicle_type=vehicle_type,
                    price=price
                )
        except Package.DoesNotExist:
            print(f"Warning: Package '{package_name}' not found")

def reverse_func(apps, schema_editor):
    VehiclePackagePrice = apps.get_model('booking', 'VehiclePackagePrice')
    VehiclePackagePrice.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0015_vehiclepackageprice'),  # Update with actual migration number
    ]
    
    operations = [
        migrations.RunPython(populate_vehicle_pricing, reverse_func),
    ]