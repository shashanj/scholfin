# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_delete_institute'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('short_name', models.CharField(max_length=20)),
            ],
        ),
    ]
