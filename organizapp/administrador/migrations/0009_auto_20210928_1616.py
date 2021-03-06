# Generated by Django 3.2.6 on 2021-09-28 19:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0008_auto_20210928_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date_event_end',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 28, 16, 16, 12, 816617), verbose_name='Fecha de baja del evento'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_event_start',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 28, 16, 16, 12, 816617), verbose_name='Fecha de alta del evento'),
        ),
    ]
