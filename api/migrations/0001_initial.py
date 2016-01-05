# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('institute_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('short_name', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
            ],
        ),
    ]
