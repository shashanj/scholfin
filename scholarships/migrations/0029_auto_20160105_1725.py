# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0028_auto_20151219_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='document',
            fields=[
                ('document_id', models.AutoField(serialize=False, primary_key=True)),
                ('document_name', models.CharField(default=b' ', max_length=250)),
            ],
        ),
        migrations.AddField(
            model_name='scholarship',
            name='display_amount',
            field=models.CharField(default=b' ', max_length=200),
        ),
        migrations.AddField(
            model_name='scholarship',
            name='display_income',
            field=models.CharField(default=b' ', max_length=200),
        ),
        migrations.AddField(
            model_name='scholarship',
            name='display_total_number_scholarship',
            field=models.CharField(default=b' ', max_length=200),
        ),
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 5, 11, 55, 38, 139000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 5, 11, 55, 38, 95000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 5, 11, 55, 38, 95000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_income',
            field=models.CharField(max_length=300),
        ),
        migrations.AddField(
            model_name='scholarship',
            name='document_required',
            field=models.ManyToManyField(to='scholarships.document'),
        ),
    ]
