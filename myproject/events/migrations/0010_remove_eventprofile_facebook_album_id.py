# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_eventprofile_facebook_album_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventprofile',
            name='facebook_album_id',
        ),
    ]
