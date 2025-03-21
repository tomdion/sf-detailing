# Generated by Django 5.1.6 on 2025-03-04 01:54

from django.db import migrations

def create_packages(apps, schema_editor):
    Package = apps.get_model('booking', 'Package')
    
    # Create packages with prices
    Package.objects.create(
        name='interior',
        display_name='Interior',
        price=50.00,
        description='Interior detailing service'
    )
    
    Package.objects.create(
        name='exterior',
        display_name='Exterior',
        price=60.00,
        description='Exterior detailing service'
    )
    
    Package.objects.create(
        name='interior_exterior',
        display_name='Interior + Exterior',
        price=100.00,
        description='Complete interior and exterior detailing service'
    )

def reverse_func(apps, schema_editor):
    Package = apps.get_model('booking', 'Package')
    Package.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0003_create_package_model'),  # Update with actual migration number
    ]
    
    operations = [
        migrations.RunPython(create_packages, reverse_func),
    ]