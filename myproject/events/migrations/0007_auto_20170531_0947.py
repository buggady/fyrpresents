# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_eventprofile_facebook_gallery_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventprofile',
            old_name='facebook_gallery_id',
            new_name='facebook_album_id',
        ),
    ]
