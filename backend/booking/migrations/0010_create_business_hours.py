# Generated manually

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_add_users_and_confirmation'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessHours',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('day', models.IntegerField(
                    choices=[
                        (0, 'Monday'),
                        (1, 'Tuesday'),
                        (2, 'Wednesday'),
                        (3, 'Thursday'),
                        (4, 'Friday'),
                        (5, 'Saturday'),
                        (6, 'Sunday')
                    ],
                    unique=True
                )),
                ('opening_time', models.TimeField()),
                ('closing_time', models.TimeField()),
                ('is_open', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Business Hours',
                'verbose_name_plural': 'Business Hours',
                'ordering': ['day'],
            },
        ),
    ]