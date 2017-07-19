# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_remove_eventideas_possible_activities'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventprofile',
            name='aftermovie_url',
            field=models.URLField(null=True, blank=True),
        ),
    ]
