# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scholarships', '0009_auto_20151025_2334'),
    ]

    operations = [
        migrations.CreateModel(
            name='loggedcount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_count', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 10, 20, 18, 184000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 26, 10, 20, 18, 184000, tzinfo=utc), blank=True),
        ),
        migrations.AddField(
            model_name='loggedcount',
            name='scholarship',
            field=models.OneToOneField(to='scholarships.scholarship'),
        ),
        migrations.AddField(
            model_name='loggedcount',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
