# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0048_auto_20160421_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 20, 46, 56, 159000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='cat',
            field=models.ForeignKey(related_name='Question_Category', blank=True, to='scholarships.Question_Category', null=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 20, 46, 56, 97000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 20, 46, 56, 112000, tzinfo=utc), blank=True),
        ),
    ]
