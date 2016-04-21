# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0047_auto_20160421_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='input_type',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 17, 42, 15, 485000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='required',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 17, 42, 15, 438000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 17, 42, 15, 438000, tzinfo=utc), blank=True),
        ),
    ]
