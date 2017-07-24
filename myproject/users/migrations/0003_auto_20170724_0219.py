# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import address.models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0007_auto_20170708_0209'),
        ('users', '0002_auto_20170531_0724'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='color_theme',
            field=models.CharField(default=b'blue', max_length=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='home_address',
            field=address.models.AddressField(related_name='home_address', blank=True, to='address.Address', null=True),
        ),
    ]
