# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0020_auto_20151030_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 30, 13, 52, 26, 14000, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 30, 13, 52, 15, 437000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 30, 13, 52, 15, 437000, tzinfo=utc), blank=True),
        ),
    ]
