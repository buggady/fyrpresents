# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20170531_0436'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventideas',
            name='facebook_event_id',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='eventideas',
            name='location',
            field=models.CharField(default=b'Unknown', max_length=140),
        ),
    ]
