# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scholarships', '0018_auto_20151213_0113'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('note_id', models.AutoField(serialize=False, primary_key=True)),
                ('note', models.TextField(default=b'')),
                ('by', models.ForeignKey(related_name='by', to=settings.AUTH_USER_MODEL)),
                ('of', models.ForeignKey(related_name='of', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 16, 54, 44, 884000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 16, 54, 44, 842000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 14, 16, 54, 44, 843000, tzinfo=utc), blank=True),
        ),
        migrations.AddField(
            model_name='note',
            name='scholarship',
            field=models.ForeignKey(related_name='note', to='scholarships.scholarship'),
        ),
    ]
