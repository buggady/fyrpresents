# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('fyr_member', 'FYR Approved members'), ('fyr_planner', 'FYR Planning Leaders'), ('fyr_developer', 'FYR Developers'))},
        ),
    ]
