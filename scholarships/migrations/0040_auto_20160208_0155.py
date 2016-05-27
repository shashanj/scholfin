# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0039_auto_20160208_0150'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='provider_contact',
            field=models.CharField(default=b' ', max_length=15),
        ),
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 7, 20, 25, 33, 377931, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 7, 20, 25, 33, 361292, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 7, 20, 25, 33, 361505, tzinfo=utc), blank=True),
        ),
    ]
