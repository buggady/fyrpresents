# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_auto_20170614_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventuserrel',
            name='fully_paid',
            field=models.BooleanField(default=False),
        ),
    ]
