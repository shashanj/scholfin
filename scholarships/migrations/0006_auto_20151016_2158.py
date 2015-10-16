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
        migrations.CreateModel(
            name='scholarshipEmails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_address', models.EmailField(max_length=254, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='scholarship',
            name='image_url',
            field=models.URLField(default=b' '),
        ),
        migrations.AddField(
            model_name='scholarship',
            name='summary',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 16, 21, 58, 46, 494698, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='meta_data',
            field=models.CharField(default=b' ', max_length=200),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 16, 21, 58, 46, 494982, tzinfo=utc), blank=True),
        ),
        migrations.AddField(
            model_name='scholarship',
            name='emails',
            field=models.ManyToManyField(to='scholarships.scholarshipEmails'),
        ),
    ]
