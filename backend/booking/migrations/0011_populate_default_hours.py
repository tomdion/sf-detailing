# Generated manually

from django.db import migrations

def create_default_hours(apps, schema_editor):
    BusinessHours = apps.get_model('booking', 'BusinessHours')
    
    default_hours = [
        # Monday through Friday: 9 AM - 9 PM
        {'day': 0, 'opening_time': '09:00', 'closing_time': '21:00', 'is_open': True},
        {'day': 1, 'opening_time': '09:00', 'closing_time': '21:00', 'is_open': True},
        {'day': 2, 'opening_time': '09:00', 'closing_time': '21:00', 'is_open': True},
        {'day': 3, 'opening_time': '09:00', 'closing_time': '21:00', 'is_open': True},
        {'day': 4, 'opening_time': '09:00', 'closing_time': '21:00', 'is_open': True},
        # Saturday: 3 PM - 9 PM
        {'day': 5, 'opening_time': '15:00', 'closing_time': '21:00', 'is_open': True},
        {'day': 6, 'opening_time': '15:00', 'closing_time': '21:00', 'is_open': True},
    ]
    
    for hours in default_hours:
        BusinessHours.objects.create(**hours)

def reverse_func(apps, schema_editor):
    BusinessHours = apps.get_model('booking', 'BusinessHours')
    BusinessHours.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0010_create_business_hours'),
    ]
    
    operations = [
        migrations.RunPython(create_default_hours, reverse_func),
    ]