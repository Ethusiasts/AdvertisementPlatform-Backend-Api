# Generated by Django 4.1.7 on 2023-04-24 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landowner', '0006_alter_landowner_company_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landowner',
            name='company_name',
            field=models.CharField(max_length=50),
        ),
    ]
