# Generated by Django 4.1.7 on 2023-05-23 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='comment',
            field=models.CharField(default=None, max_length=128),
        ),
    ]