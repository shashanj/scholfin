# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0005_auto_20151004_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='saved_scholarships',
            field=models.ManyToManyField(related_name='saved_scholarships+', to='scholarships.scholarship', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='uninterested_scholarships',
            field=models.ManyToManyField(related_name='uninterested_scholarships+', to='scholarships.scholarship', blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 8, 9, 10, 839205, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 11, 8, 9, 10, 839349, tzinfo=utc), blank=True),
        ),
    ]
