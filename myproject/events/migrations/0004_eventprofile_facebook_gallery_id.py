# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20170531_0437'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventprofile',
            name='facebook_gallery_id',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
