# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_remove_eventprofile_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventprofile',
            name='total_price',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
