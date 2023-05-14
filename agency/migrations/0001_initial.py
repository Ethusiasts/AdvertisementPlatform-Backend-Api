# Generated by Django 4.1.7 on 2023-05-03 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peak_hour', models.DecimalField(decimal_places=2, max_digits=10)),
                ('normal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('production', models.DecimalField(decimal_places=2, max_digits=10)),
                ('with_out_production', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]