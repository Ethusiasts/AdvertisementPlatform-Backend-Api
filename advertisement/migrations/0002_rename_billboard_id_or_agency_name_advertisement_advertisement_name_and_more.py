# Generated by Django 4.1.7 on 2023-05-22 20:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('advertisement', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisement',
            old_name='billBoard_id_or_agency_name',
            new_name='advertisement_name',
        ),
        migrations.RemoveField(
            model_name='advertisement',
            name='total_price',
        ),
        migrations.AddField(
            model_name='advertisement',
            name='customer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
