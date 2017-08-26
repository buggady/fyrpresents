# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0028_auto_20170725_1339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventprofile',
            name='products_for_sale',
        ),
        migrations.AlterField(
            model_name='eventprofile',
            name='facebook_event_id',
            field=models.CharField(default=datetime.datetime(2017, 7, 26, 2, 21, 18, 239993, tzinfo=utc), max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventprofile',
            name='facebook_fyr_event_id',
            field=models.CharField(default=datetime.datetime(2017, 7, 26, 2, 21, 39, 878431, tzinfo=utc), max_length=100, blank=True),
            preserve_default=False,
        ),
    ]
