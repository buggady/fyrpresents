# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_eventideas_sub_event_idea'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventideas',
            name='estimated_date',
            field=models.DateField(default=datetime.date.today, null=True, blank=True),
        ),
    ]
