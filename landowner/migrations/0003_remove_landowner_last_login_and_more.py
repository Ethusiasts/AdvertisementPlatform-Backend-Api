# Generated by Django 4.1.7 on 2023-03-30 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landowner', '0002_alter_landowner_tin_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='landowner',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='landowner',
            name='password',
        ),
        migrations.AlterField(
            model_name='landowner',
            name='tin_number',
            field=models.CharField(max_length=9),
        ),
    ]
