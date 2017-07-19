# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_eventideas_estimated_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventideas',
            name='possible_activities',
            field=models.CharField(default=b'Unknown', max_length=255, null=True, blank=True),
        ),
    ]
