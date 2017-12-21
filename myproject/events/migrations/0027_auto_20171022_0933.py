# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0010_auto_20160105_1307'),
        ('events', '0026_remove_eventprofile_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventprofile',
            name='host',
        ),
        migrations.AddField(
            model_name='eventprofile',
            name='display_photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='photologue.Photo', null=True),
        ),
        migrations.AlterField(
            model_name='eventprofile',
            name='facebook_album_id',
            field=models.CharField(default='none', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventprofile',
            name='facebook_event_id',
            field=models.CharField(default='none', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventprofile',
            name='facebook_fyr_event_id',
            field=models.CharField(default='none', max_length=100, blank=True),
            preserve_default=False,
        ),
    ]
