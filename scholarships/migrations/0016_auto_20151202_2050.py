# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0015_auto_20151202_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='apply_click',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 2, 20, 50, 54, 428000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 2, 20, 50, 54, 186000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 2, 20, 50, 54, 188000, tzinfo=utc), blank=True),
        ),
    ]
