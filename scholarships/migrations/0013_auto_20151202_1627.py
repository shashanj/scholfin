# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0012_auto_20151201_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='scholarship',
            field=models.ForeignKey(related_name='sch', to='scholarships.scholarship'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 2, 16, 27, 0, 194000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(related_name='activity', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='questionof', to='scholarships.question'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(related_name='answerby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 2, 16, 27, 0, 174000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 2, 16, 27, 0, 174000, tzinfo=utc), blank=True),
        ),
    ]
