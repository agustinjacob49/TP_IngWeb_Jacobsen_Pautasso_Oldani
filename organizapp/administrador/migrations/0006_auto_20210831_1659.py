# Generated by Django 3.2.6 on 2021-08-31 19:59

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrador', '0005_auto_20210831_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date_event_end',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 31, 16, 59, 38, 891002), verbose_name='Fecha de baja del evento'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_event_start',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 31, 16, 59, 38, 891002), verbose_name='Fecha de alta del evento'),
        ),
        migrations.AlterField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Organizador'),
        ),
    ]
