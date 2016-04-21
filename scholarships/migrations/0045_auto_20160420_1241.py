# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0044_auto_20160420_1156'),
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
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='required',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 20, 7, 7, 36, 887000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 20, 7, 7, 36, 840000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 20, 7, 7, 36, 840000, tzinfo=utc), blank=True),
        ),
        migrations.AddField(
            model_name='question',
            name='cat',
            field=models.ForeignKey(related_name='Question_Category', default=1, to='scholarships.Question_Category'),
            preserve_default=False,
        ),
    ]
