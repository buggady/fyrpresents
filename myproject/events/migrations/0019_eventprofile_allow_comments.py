# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_eventprofile_aftermovie_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventprofile',
            name='allow_comments',
            field=models.BooleanField(default=True, verbose_name=b'allow comments'),
        ),
    ]
