# Generated by Django 5.1.6 on 2025-03-04 02:04

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0005_standardize_package_names'),  # Update with actual migration number
    ]
    
    operations = [
        migrations.AddField(
            model_name='booking',
            name='package_fk',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='booking.package'
            ),
        ),
    ]