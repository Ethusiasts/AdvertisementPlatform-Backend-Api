# Generated by Django 4.1.7 on 2023-05-26 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0003_remove_agencyrating_agency_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='entity_type',
            field=models.CharField(blank=True, choices=[('Billboard', 'Billboard'), ('Agency', 'Agency')], default=None, max_length=9, null=True),
        ),
    ]
