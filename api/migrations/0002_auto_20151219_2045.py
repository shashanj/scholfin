# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institute',
            name='id',
        ),
        migrations.AlterField(
            model_name='institute',
            name='name',
            field=models.CharField(max_length=50, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='short_name',
            field=models.CharField(max_length=20),
        ),
    ]
