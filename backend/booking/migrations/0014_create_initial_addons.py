from django.db import migrations

def create_addons(apps, schema_editor):
    Addon = apps.get_model('booking', 'Addon')
    
    addons = [
        {
            'name': 'gas_cap_cleaning',
            'display_name': 'Gas Cap Cleaning',
            'price': 10.00,
            'description': 'Thorough cleaning of gas cap and surrounding area'
        },
        {
            'name': 'headlight_restoration',
            'display_name': 'Headlight Restoration',
            'price': 25.00,
            'description': 'Restore cloudy headlights to clear condition'
        },
        {
            'name': 'engine_bay_cleaning',
            'display_name': 'Engine Bay Cleaning',
            'price': 30.00,
            'description': 'Detailed cleaning of engine compartment'
        },
        {
            'name': 'pet_hair_removal',
            'display_name': 'Pet Hair Removal',
            'price': 15.00,
            'description': 'Specialized removal of embedded pet hair'
        }
    ]
    
    for addon in addons:
        Addon.objects.create(**addon)

def reverse_func(apps, schema_editor):
    Addon = apps.get_model('booking', 'Addon')
    Addon.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0013_addon_bookingaddon'),  
    ]
    
    operations = [
        migrations.RunPython(create_addons, reverse_func),
    ]