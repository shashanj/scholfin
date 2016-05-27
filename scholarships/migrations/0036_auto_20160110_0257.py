# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0035_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 9, 21, 27, 51, 680514, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='additional_links',
            field=models.CharField(default=b' ', max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 9, 21, 27, 51, 666335, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline_details',
            field=models.TextField(default=b' ', blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='other_benefits',
            field=models.TextField(default=b' ', blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 9, 21, 27, 51, 666504, tzinfo=utc), blank=True),
        ),
    ]
