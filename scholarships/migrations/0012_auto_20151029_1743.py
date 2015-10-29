# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0011_auto_20151026_2046'),
    ]

    operations = [
        migrations.CreateModel(
            name='page_source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.TextField(blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 29, 12, 13, 56, 278000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 29, 12, 13, 56, 279000, tzinfo=utc), blank=True),
        ),
        migrations.AddField(
            model_name='page_source',
            name='scholarship',
            field=models.OneToOneField(related_name='page_source', to='scholarships.scholarship'),
        ),
    ]
