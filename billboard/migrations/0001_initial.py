# Generated by Django 4.1.7 on 2023-04-28 10:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('media_agency', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('location', models.CharField(max_length=128)),
                ('image', models.ImageField(upload_to='')),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('approved', models.BooleanField(default=False)),
                ('production', models.BooleanField(default=False)),
                ('media_agency_id', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='media_agency.mediaagency')),
            ],
        ),
    ]