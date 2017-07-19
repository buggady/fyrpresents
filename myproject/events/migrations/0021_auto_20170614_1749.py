# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_eventideas_allow_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventprofile',
            name='facebook_fyr_event_id',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='eventprofile',
            name='website',
            field=models.URLField(null=True, blank=True),
        ),
    ]
