# Generated by Django 4.1.7 on 2023-06-14 13:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]