# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20160123_0325'),
        ('scholarships', '0031_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='allowed_colleges',
            field=models.ManyToManyField(to='api.Institute', blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 22, 21, 55, 14, 327000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='additional_links',
            field=models.CharField(default=b' ', max_length=500, blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 22, 21, 55, 14, 296000, tzinfo=utc), blank=True),
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
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 22, 21, 55, 14, 296000, tzinfo=utc), blank=True),
        ),
    ]
