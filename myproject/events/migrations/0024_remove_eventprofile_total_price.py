# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0023_remove_eventprofile_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventprofile',
            name='total_price',
        ),
    ]
