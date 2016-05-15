# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('party_rooms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingplace',
            name='author_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='meetingtime',
            name='author_id',
            field=models.IntegerField(default=0),
        ),
    ]
