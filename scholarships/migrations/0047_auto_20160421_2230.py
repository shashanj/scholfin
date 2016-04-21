# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0046_auto_20160420_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 17, 0, 40, 373000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='required',
            field=models.CharField(max_length=1000, blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 17, 0, 40, 311000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 17, 0, 40, 311000, tzinfo=utc), blank=True),
        ),
    ]
