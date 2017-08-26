# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0031_eventprofile_tickets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventprofile',
            name='tickets',
        ),
        migrations.AlterField(
            model_name='eventprofile',
            name='products_for_sale',
            field=models.ForeignKey(related_name='event', on_delete=django.db.models.deletion.SET_NULL, to='catalogue.Product', null=True),
        ),
    ]
