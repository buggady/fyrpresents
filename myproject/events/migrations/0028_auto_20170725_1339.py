# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '__first__'),
        ('events', '0027_auto_20170708_0307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventprofile',
            name='total_price',
        ),
        migrations.AddField(
            model_name='eventprofile',
            name='products_for_sale',
            field=models.OneToOneField(related_name='eventprofile', null=b'true', to='catalogue.Product'),
        ),
    ]
