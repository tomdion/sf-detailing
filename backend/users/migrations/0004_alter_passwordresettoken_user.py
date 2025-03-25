# Generated by Django 5.1.7 on 2025-03-25 02:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_add_2fa_and_password_reset"),
    ]

    operations = [
        migrations.AlterField(
            model_name="passwordresettoken",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reset_token",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
