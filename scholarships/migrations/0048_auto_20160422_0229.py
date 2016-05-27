# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0047_auto_20160419_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question_Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('cat_name', models.CharField(default=b' ', max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='input_type',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='required',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 20, 59, 12, 160709, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 20, 59, 12, 145309, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 20, 59, 12, 145462, tzinfo=utc), blank=True),
        ),
        migrations.AddField(
            model_name='question',
            name='cat',
            field=models.ForeignKey(related_name='Question_Category', blank=True, to='scholarships.Question_Category', null=True),
        ),
    ]
