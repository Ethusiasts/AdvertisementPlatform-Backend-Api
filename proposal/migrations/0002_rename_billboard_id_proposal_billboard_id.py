# Generated by Django 4.1.7 on 2023-06-03 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proposal',
            old_name='billBoard_id',
            new_name='billboard_id',
        ),
    ]
