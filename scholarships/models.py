from django.db import models
from django.utils import timezone
from datetime import *
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
import re

# Create your models here.

class field (models.Model):
    field_id=models.AutoField(primary_key=True)
    field_name=models.CharField(max_length=250,default=' ')
    # new class method
    def __unicode__(self):
        return self.field_name

class interest (models.Model):
    interest_id=models.AutoField(primary_key=True)
    interest_name=models.CharField(max_length=250,default=' ')
    # new class method
    def __unicode__(self):
        return self.interest_name

class caste (models.Model):
    caste_id=models.AutoField(primary_key=True)
    caste_name=models.CharField(max_length=250,default=' ')

    def __unicode__(self):
        return self.caste_name

class level(models.Model):
    level_id=models.AutoField(primary_key=True)
    level_name=models.CharField(max_length=250,default=' ')

    def __unicode__(self):
        return self.level_name

class state(models.Model):
    state_id=models.AutoField(primary_key=True)
    state_name=models.CharField(max_length=250,default=' ')

    def __unicode__(self):
        return self.state_name

class religion(models.Model):
    religion_id=models.AutoField(primary_key=True)
    religion_name=models.CharField(max_length=250,default=' ')

    def __unicode__(self):
        return self.religion_name

class abroad (models.Model):
    abroad_id=models.AutoField(primary_key=True)
    abroad_name=models.CharField(max_length=250,default=' ')
    # new class method
    def __unicode__(self):
        return self.abroad_name
# class scholarship_emails(models.Model):
#     email_address = models.EmailField(blank=True)

class scholarship(models.Model):
    scholarship_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=250,default=' ')
    offered_by=models.CharField(max_length=250,default=' ')
    total_number_scholarship=models.IntegerField(default=0)
    image_url = models.URLField(max_length=200, default=' ',blank=True)
    summary = models.TextField(blank=True)
    
    # foreign keys
    # emails = models.ManyToManyField(scholarship_emails)
    education_field=models.ManyToManyField(field)
    education_interest=models.ManyToManyField(interest,blank=True)
    education_caste=models.ManyToManyField(caste)
    education_religion=models.ManyToManyField(religion)
    education_level=models.ManyToManyField(level)
    education_state=models.ManyToManyField(state)
    education_abroad=models.ManyToManyField(abroad)

    # other filters

    gender=models.IntegerField(default=0)
    disability=models.IntegerField(default=0)
    income=models.IntegerField(default=0)

    #deadline details

    deadline=models.DateTimeField(blank=True,default=timezone.now())
    deadline_details=models.TextField(default=' ')
    deadline_type=models.IntegerField(default=0)

    # amount
    amount_frequency=models.IntegerField(default=0)
    amount_period=models.IntegerField(default=0)
    amount=models.IntegerField(default=0)
    other_benefits=models.TextField(default=' ')
    currency=models.IntegerField(default=0)

    # type govt,trust,competitions

    scholarship_type=models.IntegerField(default=0)

    # time

    timestamp=models.DateTimeField(default=timezone.now(),blank=True)

    # application mode of scholarship

    application_mode=models.IntegerField(default=0)

    eligibility=models.TextField(default=' ')
    about=models.TextField(default=' ')
    procedure=models.TextField(default=' ')
    contact_details=models.TextField(default=' ')
    apply_link=models.CharField(max_length=500,default=' ')
    additional_links=models.CharField(max_length=500,default=' ')

    meta_data=models.CharField(max_length=200,default=' ')
    meta_title=models.CharField(max_length=65,default=' ')

    def __unicode__ (self):
        return self.name;

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.scholarship_id,))

    def get_absolute_url(self):
        x = re.sub('[^A-Za-z0-9]+','-',re.sub('[^A-Za-z0-9]+',' ',self.name).strip(' '))
        return "/scholarship-details/"+x ;

class loggedcount(models.Model):
    scholarship = models.OneToOneField(scholarship)
    user = models.ManyToManyField(User)
    user_count = models.BigIntegerField(default=0)

    def __unicode__ (self):
        return self.scholarship.name
        
class UserProfile(models.Model):
    # linking user profile to a user
    user = models.OneToOneField(User, related_name='profile')
    auth_type = models.CharField(max_length=200,blank=False,default=None)
    #additional user information
    user_state = models.ForeignKey(state)
    user_level = models.ForeignKey(level)
    user_caste = models.ForeignKey(caste)
    user_religion = models.ForeignKey(religion)
    user_income = models.CharField(max_length=200,blank=False)
    user_interest=models.ManyToManyField(interest,blank=True)
    user_type = models.CharField(max_length=200,blank=True)
    user_abroad = models.ForeignKey(abroad)
    user_field = models.ForeignKey(field)
    user_gender = models.IntegerField(blank=False)
    user_disability = models.IntegerField(blank=False)


    def __unicode__(self):
        return self.user.username





class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

class page_source(models.Model):
    source = models.TextField(blank=True)
    scholarship = models.OneToOneField(scholarship, related_name='page_source')

    def __unicode__ (self):
        return self.scholarship.name