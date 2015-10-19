# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0008_auto_20151019_1918'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='scholarshipEmails',
            new_name='scholarshipEmail',
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 19, 20, 49, 574388, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 19, 20, 49, 574678, tzinfo=utc), blank=True),
        ),
    ]
