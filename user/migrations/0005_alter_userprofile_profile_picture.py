# Generated by Django 4.1.7 on 2023-06-13 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_rename_user_id_userprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.URLField(default=None, max_length=1000),
        ),
    ]
