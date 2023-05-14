# Generated by Django 4.1.7 on 2023-05-03 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media_agency', '0001_initial'),
        ('billboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billboard',
            name='media_agency_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='media_agency.mediaagency'),
        ),
    ]
