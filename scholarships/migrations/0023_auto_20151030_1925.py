# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0022_auto_20151030_1924'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scholarship',
            old_name='update',
            new_name='updated_time',
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 30, 13, 55, 18, 416000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 30, 13, 55, 18, 416000, tzinfo=utc), blank=True),
        ),
    ]
