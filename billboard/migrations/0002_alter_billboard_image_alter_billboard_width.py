# Generated by Django 4.1.7 on 2023-06-02 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billboard',
            name='image',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='billboard',
            name='width',
            field=models.IntegerField(max_length=500),
        ),
    ]