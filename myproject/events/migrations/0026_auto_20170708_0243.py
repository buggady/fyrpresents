# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import address.models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0007_auto_20170708_0209'),
        ('events', '0025_auto_20170708_0225'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventprofile',
            name='new_address',
            field=address.models.AddressField(related_name='new_address', blank=True, to='address.Address', null=True),
        ),
    ]
