import django
from django.conf import settings

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scholfin.settings")
django.setup()
from django.core.management.base import BaseCommand, CommandError
from django.core.management import execute_from_command_line
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required

#from django.db.models import Q
from django.views.decorators.cache import cache_control
from scholarships.models import *
import re
from datetime import datetime,timedelta
import urllib # Python URL functions
import urllib2 # Python URL functions
from datetime import date
from django.utils import timezone

auth_key="103486AfvSPCxmd3nE56aa5ba6"
message = " people just applied for your Scholarship" # Your message to send.
sender = "918239026608" # Sender ID,While using route4 sender id should be 6 characters long.
route = "default" # Define route
url = "http://api.msg91.com/api/sendhttp.php" # API URL

today_date = timezone.now()
today_activity = activity.objects.filter(timestamp__lte=today_date).filter(activity='just applied for your Scholarship')
# print today_date

print today_activity

provider_dict = {'key':0}

for i in today_activity:
    curr_provider_email = i.scholarship.provider_email
    if provider_dict.has_key(curr_provider_email) == True:
        provider_dict[curr_provider_email] = provider_dict[curr_provider_email] +1
    else:
        provider_dict[curr_provider_email]=1

print provider_dict
import sendgrid
sg_username = "scholfin"
sg_password = "sameer1234"

for key in provider_dict:
    mobile_no = scholarship.objects.values_list('provider_contact', flat=True).filter(provider_email=key)
    # Prepare you post parameters
    text_msg = str(provider_dict[key]) + message
    values = {
          'authkey' : auth_key,
          'mobiles' : mobile_no,
          'message' : text_msg,
          'sender' : sender,
          'route' : route
          }
    postdata = urllib.urlencode(values) # URL encoding the data here.
    req = urllib2.Request(url, postdata)
    response = urllib2.urlopen(req)
    

    sg = sendgrid.SendGridClient(sg_username, sg_password)
    message = sendgrid.Mail()

    message.set_from("thescholfin@gmail.com")
    message.set_subject("Today's Applicants on your Scholarship!")
    message.set_text(text_msg)
    message.add_to(key)
    try:
        status, msg = sg.send(message)
        print msg
        # print count
    except:
        print 'error'
                # pass

output = response.read() # Get Response

print output # Print Response
