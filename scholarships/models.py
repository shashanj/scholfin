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


class document(models.Model):
    document_id=models.AutoField(primary_key=True)
    document_name=models.CharField(max_length=250,default=' ')

    def __unicode__(self):
        return self.document_name

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
    display_total_number_scholarship = models.CharField(max_length=200,default=' ')
    image_url = models.URLField(max_length=200,blank=True)
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
    document_required=models.ManyToManyField(document, blank=True)
    provider_email = models.EmailField(blank=True)
    # other filters

    gender=models.IntegerField(default=0)
    disability=models.IntegerField(default=0)
    income=models.IntegerField(default=0)
    display_income = models.CharField(max_length=200,default=' ')

    #deadline details

    deadline=models.DateTimeField(blank=True,default=timezone.now())
    deadline_details=models.TextField(default=' ')
    deadline_type=models.IntegerField(default=0)

    # amount
    amount_frequency=models.IntegerField(default=0)
    amount_period=models.IntegerField(default=0)
    amount=models.IntegerField(default=0)
    display_amount = models.CharField(max_length=200,default=' ')
    other_benefits=models.TextField(default=' ')
    currency=models.IntegerField(default=0)

    # type govt,trust,competitions

    scholarship_type=models.IntegerField(default=0)

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

    organic_view = models.IntegerField(default=0)
    logged_view = models.IntegerField(default=0)
    apply_click = models.IntegerField(default=0)

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
    user_income = models.CharField(max_length=300,blank=False)
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
    search_fields = ['name','contact_details']
    list_filter = ['education_caste__caste_name','education_religion__religion_name','education_level__level_name','education_field__field_name','education_abroad__abroad_name','gender','disability','deadline_type','currency','scholarship_type','application_mode','education_state__state_name',]


class page_source(models.Model):
    source = models.TextField(blank=True)
    scholarship = models.OneToOneField(scholarship, related_name='page_source')

    def __unicode__ (self):
        return self.scholarship.name

class Provider(models.Model):
    # linking provider profile to a user
    user = models.OneToOneField(User, related_name='provider')
    user_type = models.IntegerField(default=0,blank=True)
    auth_type = models.CharField(max_length=200,blank=False,default=None)
    scholarship = models.ManyToManyField(scholarship,blank=True)

    def __unicode__ (self):
        return self.user.username

class question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=1000,default=' ')
    question_type = models.IntegerField(default=0)
    expected_answers = models.TextField(blank=True)
    scholarship = models.ForeignKey(scholarship,related_name='scholarship')

    def __unicode__(self):
        return self.question

class answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    answer = models.TextField(default=' ')
    question = models.ForeignKey(question,related_name='questionof')
    user =  models.ForeignKey(User,related_name='answerby')

    def __unicode__(self):
        return self.user.first_name + ' answered ' + self.question.question

class activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,related_name='activity')
    scholarship = models.ForeignKey(scholarship,related_name='sch')
    activity = models.TextField(blank=True)
    timestamp=models.DateTimeField(default=timezone.now(),blank=True)

    def __unicode__(self):
        return  self.user.username + self.activity

class Applicant(models.Model):
    applicant_id = models.AutoField(primary_key=True)
    applicant = models.ManyToManyField(User,related_name='applicant')
    scholarship = models.OneToOneField(scholarship,related_name='appforscholarship')
    count = models.BigIntegerField(default=0)

    def __unicode__(self):
        return self.scholarship.name

class ShortList(models.Model):
    shortlist_id = models.AutoField(primary_key=True)
    shortlist = models.ManyToManyField(User,related_name='shortlist')
    scholarship = models.OneToOneField(scholarship,related_name='slforscholarship')
    count = models.BigIntegerField(default=0)

    def __unicode__(self):
        return self.scholarship.name

class Selected(models.Model):
    selected_id = models.AutoField(primary_key=True)
    selected = models.ManyToManyField(User,related_name='selected')
    scholarship = models.OneToOneField(scholarship,related_name='selforscholarship')
    count = models.BigIntegerField(default=0)

    def __unicode__(self):
        return self.scholarship.name

class Rejected(models.Model):
    rejected_id = models.AutoField(primary_key=True)
    rejected = models.ManyToManyField(User,related_name='rejected')
    scholarship = models.OneToOneField(scholarship,related_name='rejforscholarship')
    count = models.BigIntegerField(default=0)

    def __unicode__(self):
        return self.scholarship.name

class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    note = models.TextField(default='')
    scholarship = models.ForeignKey(scholarship,related_name='note')
    by =  models.ForeignKey(User,related_name='by')
    of = models.ForeignKey(User,related_name='of')

    def __unicode__(self):
        return self.by.email + ' took note on ' + self.of.email +' for ' + self.scholarship.name 