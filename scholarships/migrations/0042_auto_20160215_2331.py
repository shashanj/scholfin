# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0041_auto_20160208_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='points',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 15, 18, 1, 29, 794114, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 15, 18, 1, 29, 778916, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 15, 18, 1, 29, 779066, tzinfo=utc), blank=True),
        ),
    ]
