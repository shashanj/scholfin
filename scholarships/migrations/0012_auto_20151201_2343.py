# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scholarships', '0011_auto_20151026_2046'),
    ]

    operations = [
        migrations.CreateModel(
            name='activity',
            fields=[
                ('activity_id', models.AutoField(serialize=False, primary_key=True)),
                ('activity', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2015, 12, 1, 23, 43, 57, 893000, tzinfo=utc), blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='answer',
            fields=[
                ('answer_id', models.AutoField(serialize=False, primary_key=True)),
                ('answer', models.CharField(default=b' ', max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='page_source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_type', models.IntegerField(default=0, blank=True)),
                ('auth_type', models.CharField(default=None, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='question',
            fields=[
                ('question_id', models.AutoField(serialize=False, primary_key=True)),
                ('question', models.CharField(default=b' ', max_length=1000)),
                ('question_type', models.IntegerField(default=0)),
                ('expected_answers', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='scholarship',
            name='logged_view',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='scholarship',
            name='organic_view',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 1, 23, 43, 57, 877000, tzinfo=utc), blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='image_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 1, 23, 43, 57, 877000, tzinfo=utc), blank=True),
        ),
        migrations.AddField(
            model_name='question',
            name='scholarship',
            field=models.ForeignKey(related_name='scholarship', to='scholarships.scholarship'),
        ),
        migrations.AddField(
            model_name='provider',
            name='scholarship',
            field=models.ManyToManyField(to='scholarships.scholarship', blank=True),
        ),
        migrations.AddField(
            model_name='provider',
            name='user',
            field=models.OneToOneField(related_name='provider', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='page_source',
            name='scholarship',
            field=models.OneToOneField(related_name='page_source', to='scholarships.scholarship'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.OneToOneField(related_name='questionof', to='scholarships.question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.OneToOneField(related_name='answerby', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='scholarship',
            field=models.OneToOneField(related_name='sch', to='scholarships.scholarship'),
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.OneToOneField(related_name='activity', to=settings.AUTH_USER_MODEL),
        ),
    ]
