# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import address.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_eventprofile_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventprofile',
            name='address',
            field=address.models.AddressField(related_name='address', blank=True, to='address.Address', null=True),
        ),
    ]
