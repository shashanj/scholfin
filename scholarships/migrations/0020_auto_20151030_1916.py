# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0019_auto_20151030_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scholarship',
            name='update',
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 30, 13, 46, 16, 989000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 30, 13, 46, 16, 989000, tzinfo=utc), blank=True),
        ),
    ]
