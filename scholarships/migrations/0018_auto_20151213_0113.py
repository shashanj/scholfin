# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scholarships', '0017_auto_20151208_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rejected',
            fields=[
                ('rejected_id', models.AutoField(serialize=False, primary_key=True)),
                ('count', models.BigIntegerField(default=0)),
                ('rejected', models.ManyToManyField(related_name='rejected', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 12, 19, 43, 27, 129000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 12, 19, 43, 27, 87000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 12, 19, 43, 27, 88000, tzinfo=utc), blank=True),
        ),
        migrations.AddField(
            model_name='rejected',
            name='scholarship',
            field=models.OneToOneField(related_name='rejforscholarship', to='scholarships.scholarship'),
        ),
    ]
