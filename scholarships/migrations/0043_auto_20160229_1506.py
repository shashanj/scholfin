# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0042_auto_20160215_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='important_point',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 29, 9, 36, 26, 250253, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 29, 9, 36, 26, 235238, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 29, 9, 36, 26, 235377, tzinfo=utc), blank=True),
        ),
    ]
