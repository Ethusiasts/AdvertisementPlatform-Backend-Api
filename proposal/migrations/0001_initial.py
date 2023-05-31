# Generated by Django 4.1.7 on 2023-05-31 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('billboard', '0006_billboard_monthly_rate_per_sq_alter_billboard_status'),
        ('media_agency', '0001_initial'),
        ('advertisement', '0003_alter_advertisement_advertisement_file'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('approved', models.BooleanField(default=False)),
                ('advertisement_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisement.advertisement')),
                ('billBoard_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='billboard.billboard')),
                ('media_agency_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='media_agency.mediaagency')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
