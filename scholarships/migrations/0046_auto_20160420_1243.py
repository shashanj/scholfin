# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0045_auto_20160420_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 20, 7, 13, 45, 580000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='cat',
            field=models.ForeignKey(related_name='Question_Category', blank=True, to='scholarships.Question_Category'),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 20, 7, 13, 45, 533000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 20, 7, 13, 45, 533000, tzinfo=utc), blank=True),
        ),
    ]
