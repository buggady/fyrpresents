# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import oscar.core.utils


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partner',
            options={'ordering': ('name', 'code'), 'verbose_name': 'Fulfillment partner', 'verbose_name_plural': 'Fulfillment partners', 'permissions': (('dashboard_access', 'Can access dashboard'),)},
        ),
        migrations.AlterField(
            model_name='partner',
            name='users',
            field=models.ManyToManyField(related_name='partners', verbose_name='Users', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='stockrecord',
            name='price_currency',
            field=models.CharField(default=oscar.core.utils.get_default_currency, max_length=12, verbose_name='Currency'),
        ),
    ]
