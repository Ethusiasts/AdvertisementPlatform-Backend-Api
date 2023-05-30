# Generated by Django 4.1.7 on 2023-05-26 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0004_alter_rating_entity_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='entity_type',
            field=models.CharField(blank=True, choices=[('Billboard', 'Billboard'), ('Agency', 'Agency')], max_length=9, null=True),
        ),
    ]