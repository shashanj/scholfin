# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='abroad',
            fields=[
                ('abroad_id', models.AutoField(serialize=False, primary_key=True)),
                ('abroad_name', models.CharField(default=b' ', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='caste',
            fields=[
                ('caste_id', models.AutoField(serialize=False, primary_key=True)),
                ('caste_name', models.CharField(default=b' ', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='field',
            fields=[
                ('field_id', models.AutoField(serialize=False, primary_key=True)),
                ('field_name', models.CharField(default=b' ', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='interest',
            fields=[
                ('interest_id', models.AutoField(serialize=False, primary_key=True)),
                ('interest_name', models.CharField(default=b' ', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='level',
            fields=[
                ('level_id', models.AutoField(serialize=False, primary_key=True)),
                ('level_name', models.CharField(default=b' ', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='religion',
            fields=[
                ('religion_id', models.AutoField(serialize=False, primary_key=True)),
                ('religion_name', models.CharField(default=b' ', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='scholarship',
            fields=[
                ('scholarship_id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(default=b' ', max_length=250)),
                ('offered_by', models.CharField(default=b' ', max_length=250)),
                ('total_number_scholarship', models.IntegerField(default=0)),
                ('gender', models.IntegerField(default=0)),
                ('disability', models.IntegerField(default=0)),
                ('income', models.IntegerField(default=0)),
                ('deadline', models.DateTimeField(default=datetime.datetime(2015, 8, 18, 18, 56, 24, 95107, tzinfo=utc), blank=True)),
                ('deadline_details', models.TextField(default=b' ')),
                ('deadline_type', models.IntegerField(default=0)),
                ('amount_frequency', models.IntegerField(default=0)),
                ('amount_period', models.IntegerField(default=0)),
                ('amount', models.IntegerField(default=0)),
                ('other_benefits', models.TextField(default=b' ')),
                ('currency', models.IntegerField(default=0)),
                ('scholarship_type', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2015, 8, 18, 18, 56, 24, 95241, tzinfo=utc), blank=True)),
                ('application_mode', models.IntegerField(default=0)),
                ('eligibility', models.TextField(default=b' ')),
                ('about', models.TextField(default=b' ')),
                ('procedure', models.TextField(default=b' ')),
                ('contact_details', models.TextField(default=b' ')),
                ('apply_link', models.CharField(default=b' ', max_length=500)),
                ('additional_links', models.CharField(default=b' ', max_length=500)),
                ('meta_data', models.CharField(default=b' ', max_length=170)),
                ('meta_title', models.CharField(default=b' ', max_length=65)),
                ('education_abroad', models.ManyToManyField(to='scholarships.abroad')),
                ('education_caste', models.ManyToManyField(to='scholarships.caste')),
                ('education_field', models.ManyToManyField(to='scholarships.field')),
                ('education_interest', models.ManyToManyField(to='scholarships.interest')),
                ('education_level', models.ManyToManyField(to='scholarships.level')),
                ('education_religion', models.ManyToManyField(to='scholarships.religion')),
            ],
        ),
        migrations.CreateModel(
            name='state',
            fields=[
                ('state_id', models.AutoField(serialize=False, primary_key=True)),
                ('state_name', models.CharField(default=b' ', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_income', models.CharField(max_length=200)),
                ('user_type', models.CharField(max_length=200, blank=True)),
                ('user_gender', models.IntegerField()),
                ('user_disability', models.IntegerField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('user_abroad', models.ForeignKey(to='scholarships.abroad')),
                ('user_caste', models.ForeignKey(to='scholarships.caste')),
                ('user_field', models.ForeignKey(to='scholarships.field')),
                ('user_interest', models.ManyToManyField(to='scholarships.interest', blank=True)),
                ('user_level', models.ForeignKey(to='scholarships.level')),
                ('user_religion', models.ForeignKey(to='scholarships.religion')),
                ('user_state', models.ForeignKey(to='scholarships.state')),
            ],
        ),
        migrations.AddField(
            model_name='scholarship',
            name='education_state',
            field=models.ManyToManyField(to='scholarships.state'),
        ),
    ]
