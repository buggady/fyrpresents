# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_eventideas_possible_activities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventideas',
            name='possible_activities',
        ),
    ]
