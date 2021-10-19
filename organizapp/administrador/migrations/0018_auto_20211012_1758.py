# Generated by Django 3.2.6 on 2021-10-12 20:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0017_merge_20211012_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date_event_end',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 17, 58, 54, 357673), verbose_name='Fecha de baja del evento'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_event_start',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 12, 17, 58, 54, 357673), verbose_name='Fecha de alta del evento'),
        ),
    ]