# Generated by Django 4.1.7 on 2023-06-14 13:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0002_alter_proposal_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]