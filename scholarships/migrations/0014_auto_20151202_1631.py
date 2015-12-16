# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0013_auto_20151202_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 2, 16, 31, 16, 572000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=models.TextField(default=b' '),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 2, 16, 31, 16, 552000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 2, 16, 31, 16, 552000, tzinfo=utc), blank=True),
        ),
    ]
