# Generated by Django 3.2.6 on 2021-10-12 04:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0014_auto_20211012_0429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date_event_end',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 4, 29, 57, 475189), verbose_name='Fecha de baja del evento'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_event_start',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 4, 29, 57, 475159), verbose_name='Fecha de alta del evento'),
        ),
    ]