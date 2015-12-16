# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scholarships', '0014_auto_20151202_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('applicant_id', models.AutoField(serialize=False, primary_key=True)),
                ('count', models.BigIntegerField(default=0)),
                ('applicant', models.ManyToManyField(related_name='applicant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Selected',
            fields=[
                ('selected_id', models.AutoField(serialize=False, primary_key=True)),
                ('count', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ShortList',
            fields=[
                ('shortlist_id', models.AutoField(serialize=False, primary_key=True)),
                ('count', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 2, 19, 45, 36, 735000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 2, 19, 45, 36, 715000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 2, 19, 45, 36, 715000, tzinfo=utc), blank=True),
        ),
        migrations.AddField(
            model_name='shortlist',
            name='scholarship',
            field=models.OneToOneField(related_name='slforscholarship', to='scholarships.scholarship'),
        ),
        migrations.AddField(
            model_name='shortlist',
            name='shortlist',
            field=models.ManyToManyField(related_name='shortlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='selected',
            name='scholarship',
            field=models.OneToOneField(related_name='selforscholarship', to='scholarships.scholarship'),
        ),
        migrations.AddField(
            model_name='selected',
            name='selected',
            field=models.ManyToManyField(related_name='selected', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='applicant',
            name='scholarship',
            field=models.OneToOneField(related_name='appforscholarship', to='scholarships.scholarship'),
        ),
    ]
