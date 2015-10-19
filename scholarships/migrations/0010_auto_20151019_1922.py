# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0009_auto_20151019_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 19, 22, 34, 118020, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 19, 22, 34, 118159, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarshipemail',
            name='email_address',
            field=models.EmailField(max_length=254),
        ),
    ]
