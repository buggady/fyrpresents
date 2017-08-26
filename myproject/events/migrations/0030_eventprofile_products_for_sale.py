# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '__first__'),
        ('events', '0029_auto_20170726_0221'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventprofile',
            name='products_for_sale',
            field=models.ForeignKey(related_name='event', to='catalogue.Product', null=True),
        ),
    ]
