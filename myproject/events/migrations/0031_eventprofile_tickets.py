# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '__first__'),
        ('events', '0030_eventprofile_products_for_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventprofile',
            name='tickets',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='catalogue.Product', null=True),
        ),
    ]
