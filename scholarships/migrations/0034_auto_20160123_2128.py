# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scholarships', '0033_auto_20160123_0330'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDocuments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('files', models.FileField(upload_to=b'files', blank=True)),
                ('docs', models.ForeignKey(to='scholarships.document')),
                ('user', models.ForeignKey(to='scholarships.UserProfile')),
            ],
        ),
        migrations.AlterField(
            model_name='activity',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 23, 15, 58, 26, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 23, 15, 58, 25, 953000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 23, 15, 58, 25, 969000, tzinfo=utc), blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_documents',
            field=models.ManyToManyField(to='scholarships.document', through='scholarships.UserDocuments', blank=True),
        ),
    ]
