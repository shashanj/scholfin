# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0048_auto_20160422_0229'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registered_User',
            fields=[
                ('register_user_id', models.AutoField(serialize=False, primary_key=True)),
                ('registration_no', models.IntegerField(default=0)),
                ('first_name', models.CharField(default='', max_length=25)),
                ('last_name', models.CharField(default='', max_length=25)),
                ('father_name', models.CharField(default='', max_length=25)),
            ],
        ),
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 26, 10, 55, 20, 651601, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 26, 10, 55, 20, 634447, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 26, 10, 55, 20, 634605, tzinfo=utc), blank=True),
        ),
    ]
