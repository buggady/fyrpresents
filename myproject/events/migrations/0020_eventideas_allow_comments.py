# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_eventprofile_allow_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventideas',
            name='allow_comments',
            field=models.BooleanField(default=True, verbose_name=b'allow comments'),
        ),
    ]
