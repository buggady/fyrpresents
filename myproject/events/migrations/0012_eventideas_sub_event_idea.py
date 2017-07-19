# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_eventprofile_facebook_album_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventideas',
            name='sub_event_idea',
            field=models.BooleanField(default=False),
        ),
    ]
