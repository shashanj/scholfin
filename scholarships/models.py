from django.db import models
from django.utils import timezone
from datetime import *
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.contrib.auth.models import User
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

class scholarship(models.Model):
	scholarship_id=models.AutoField(primary_key=True)
	name=models.CharField(max_length=250,default=' ')
	offered_by=models.CharField(max_length=250,default=' ')
	total_number_scholarship=models.IntegerField(default=0)

	# foreign keys

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

	meta_data=models.CharField(max_length=170,default=' ')
	meta_title=models.CharField(max_length=65,default=' ')

	def __unicode__ (self):
		return self.name;

	def get_absolute_url(self):
		x = re.sub('[^A-Za-z0-9]+','-',re.sub('[^A-Za-z0-9]+',' ',self.name).strip(' '))
		return "/scholarship-details/"+x ;

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
	saved_scholarships = models.ManyToManyField(scholarship,blank=True,related_name='saved_scholarships+')
	uninterested_scholarships = models.ManyToManyField(scholarship,blank=True,related_name='uninterested_scholarships+')


	def __unicode__(self):
		return self.user.username





class MyModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
	}
