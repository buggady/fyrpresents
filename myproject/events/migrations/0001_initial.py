# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import django.db.models.deletion
from django.conf import settings
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_auto_20160715_0028'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photologue', '0010_auto_20160105_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventIdeas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote_score', models.IntegerField(default=0, db_index=True)),
                ('num_vote_up', models.PositiveIntegerField(default=0, db_index=True)),
                ('num_vote_down', models.PositiveIntegerField(default=0, db_index=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(unique=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('location', models.CharField(default=b'Unknown', max_length=140)),
                ('facebook_event_id', models.CharField(max_length=100, null=True, blank=True)),
                ('estimated_cost', models.IntegerField(default=b'0')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event Idea',
                'verbose_name_plural': 'Event Ideas',
            },
        ),
        migrations.CreateModel(
            name='EventProfile',
            fields=[
                ('event', annoying.fields.AutoOneToOneField(related_name='profile', primary_key=True, serialize=False, to='schedule.Event')),
                ('slug', autoslug.fields.AutoSlugField(unique=True)),
                ('category', models.CharField(default=b'general', max_length=14, choices=[(b'general', b'General'), (b'vacation', b'Vacation'), (b'festival', b'Festival'), (b'camping', b'Camping'), (b'entertainment', b'Entertainment'), (b'show', b'Show')])),
                ('private', models.BooleanField(default=True)),
                ('location', models.CharField(default=b"Don't Know", max_length=140)),
                ('total_price', models.IntegerField(default=b'0')),
                ('facebook_event_id', models.CharField(max_length=100, null=True, blank=True)),
                ('gallery', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='photologue.Gallery', null=True)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Event Profile',
                'verbose_name_plural': 'Event Profiles',
            },
        ),
        migrations.CreateModel(
            name='EventUserRel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approved', models.BooleanField(default=False)),
                ('amount_paid', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('event', models.ForeignKey(to='schedule.Event')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
