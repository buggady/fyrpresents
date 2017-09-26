# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170531_0724'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='color_theme',
            field=models.CharField(default=b'blue', max_length=10),
        ),
    ]
