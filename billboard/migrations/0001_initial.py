# Generated by Django 4.1.7 on 2023-06-16 01:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Billboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daily_rate_per_sq', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('image', models.URLField(max_length=1000)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('approved', models.PositiveIntegerField(choices=[(0, 0), (1, 1), (2, 2)], default=1)),
                ('production', models.DecimalField(decimal_places=2, default=None, max_digits=11)),
                ('paid', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('Free', 'Free'), ('Occupied', 'Occupied')], default=None, max_length=8)),
                ('description', models.TextField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('file', models.URLField(default='')),
                ('adult_content', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('media_agency_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
