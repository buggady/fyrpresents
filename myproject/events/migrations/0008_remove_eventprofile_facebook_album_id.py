# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20170531_0947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventprofile',
            name='facebook_album_id',
        ),
    ]
