# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CachedResult',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('need_calc', models.BooleanField(default=True)),
                ('result_rating', models.IntegerField(null=True)),
                ('participants', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-result_rating'],
            },
        ),
        migrations.CreateModel(
            name='Conflict',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='MeetingPlace',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('description', models.TextField(verbose_name='описание места')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MeetingTime',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('description', models.TextField(verbose_name='описание места')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlaceVote',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('possibility', models.IntegerField(choices=[(0, 'не задано'), (3, 'подходит'), (1, 'не подходит'), (2, 'возможно, подходит')], default=0)),
                ('rating', models.IntegerField(choices=[(0, 'не задано'), (3, 'одобрительно'), (1, 'неодобрительно'), (2, 'нейтрально')], default=0)),
                ('place', models.ForeignKey(to='party_rooms.MeetingPlace')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('usermade', models.BooleanField(default=True)),
                ('admin_id', models.IntegerField(null=True)),
                ('pass_hash', models.CharField(null=True, max_length=32)),
                ('description', models.CharField(null=True, max_length=255)),
                ('room_users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TimeVote',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('possibility', models.IntegerField(choices=[(0, 'не задано'), (3, 'подходит'), (1, 'не подходит'), (2, 'возможно, подходит')], default=0)),
                ('rating', models.IntegerField(choices=[(0, 'не задано'), (3, 'одобрительно'), (1, 'неодобрительно'), (2, 'нейтрально')], default=0)),
                ('time', models.ForeignKey(to='party_rooms.MeetingTime')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserCachedResult',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('need_calc', models.BooleanField(default=True)),
                ('result_rating', models.IntegerField(null=True)),
                ('is_possible', models.BooleanField(default=True)),
                ('place', models.ForeignKey(to='party_rooms.MeetingPlace')),
                ('time', models.ForeignKey(to='party_rooms.MeetingTime')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='meetingtime',
            name='room',
            field=models.ForeignKey(to='party_rooms.Room'),
        ),
        migrations.AddField(
            model_name='meetingplace',
            name='room',
            field=models.ForeignKey(to='party_rooms.Room'),
        ),
        migrations.AddField(
            model_name='conflict',
            name='place',
            field=models.ForeignKey(to='party_rooms.MeetingPlace'),
        ),
        migrations.AddField(
            model_name='conflict',
            name='time',
            field=models.ForeignKey(to='party_rooms.MeetingTime'),
        ),
        migrations.AddField(
            model_name='cachedresult',
            name='place',
            field=models.ForeignKey(to='party_rooms.MeetingPlace'),
        ),
        migrations.AddField(
            model_name='cachedresult',
            name='time',
            field=models.ForeignKey(to='party_rooms.MeetingTime'),
        ),
        migrations.AlterUniqueTogether(
            name='meetingtime',
            unique_together=set([('description', 'room')]),
        ),
        migrations.AlterUniqueTogether(
            name='meetingplace',
            unique_together=set([('description', 'room')]),
        ),
    ]
