# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_eventuserrel_fully_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventprofile',
            name='location',
        ),
    ]
