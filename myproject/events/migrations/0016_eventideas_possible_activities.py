# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_remove_eventideas_possible_activities'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventideas',
            name='possible_activities',
            field=models.CharField(default=b'Unknown', max_length=255, null=True, blank=True),
        ),
    ]
