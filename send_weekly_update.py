import django
from django.conf import settings
# from scholarships import scholarships_defaults
#settings.configure(default_settings=scholarships_defaults, DEBUG=True)
# django.setup()
import os, sys
# sys.path.append(os.getcwd())
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
#from django.core.mail import send_mail

#from forms import ScholarshipForm

# print 'yo'
# # if __name__ == '__main__': 

user = User.objects.all().order_by('id')
# print user
# print [u.email for u in user]
count = 0
for u in user:

    count+=1
    if u.is_superuser==0 or u.is_staff==0:
        mail_message = ""
        # print 'user'
        # print u.email
        # print u.username
        #em = 'palanshagarwal@gmail.com'
        user_d = UserProfile.objects.filter(user__email=u.email)
        if len(user_d)!=0 :
            user_d = user_d[0]

            
            user_table = {
                'state':user_d.user_state,
                'level':user_d.user_level,
                'religion':user_d.user_religion,
                'caste':user_d.user_caste,
                'field':user_d.user_field,
                'abroad':user_d.user_abroad,
                'gender':user_d.user_gender,

            }

            now = datetime.now()
            sevendaytimestamp = now - timedelta(days=7)

            scholarships = scholarship.objects.filter(education_state__state_name=user_table['state']).filter(
                education_level__level_name=user_table['level']).filter(education_religion__religion_name=user_table['religion']).filter(
                education_caste__caste_name=user_table['caste']).filter(education_field__field_name=user_table['field']).filter(timestamp__gte=sevendaytimestamp)
            scholarship_l=[]
            for s in scholarships:
                matched=0;
                interests=interest.objects.filter(scholarship=s)
                interests_count=interest.objects.filter(scholarship=s).count()
                user_interest=interest.objects.filter(userprofile=user_d)
                if interests_count==0:
                    scholarship_l.append(s)
                else :
                    for intrst in interests:
                        for intrst_u in user_interest:
                            if intrst==intrst_u:
                                matched=1
                    if matched==1:
                        scholarship_l.append(s)
            #print len(scholarship_l)
            scholarship_g=[]
            if user_d.user_gender ==1:
                scholarship_g=scholarship_l
            else :
                for s in scholarship_l:
                    #print s.gender
                    if s.gender == 0:
                        scholarship_g.append(s)

            scholarship_a=[]
            country = abroad.objects.filter(userprofile=user_d)
            c=country[0]
            c=str(c)

            if c==("India"):
                for s in scholarship_g:
                    country = abroad.objects.filter(scholarship=s)
                    country_count = abroad.objects.filter(scholarship=s).count()
                    if(country_count==1):
                        if(str(country[0])== 'India'):
                            scholarship_a.append(s)
            else:
                scholarship_a = scholarship_g

            scholarship_d=[]
            if user_d.user_disability == 0:
                for s in scholarship_a:
                    if s.disability !=1:
                        scholarship_d.append(s)
            else:
                scholarship_d=scholarship_a

            mail_body_1 = "<tr><td align=\"left\" class=\"padding-meta\" style=\"padding: 0 0 5px 25px; font-size: 13px; font-family: Helvetica, Arial, sans-serif; font-weight: normal; color: red;\">"
            #add deadline to 1
            mail_body_6 = "<tr><td align=\"left\" class=\"padding-meta\" style=\"padding: 0 0 5px 25px; font-size: 13px; font-family: Helvetica, Arial, sans-serif; font-weight: normal; color: green;\">"
            #add amount
            mail_body_2 = "</td></tr><tr><td align=\"left\" class=\"padding-copy\" style=\"padding: 0 0 5px 25px; font-size: 22px; font-family: Helvetica, Arial, sans-serif; font-weight: normal; color: #55bbea;\">"
            #add name to 2
            mail_body_3 = "</td></tr> <tr><td align=\"left\" class=\"padding-copy\" style=\"padding: 10px 0 15px 25px; font-size: 16px; line-height: 24px; font-family: Helvetica, Arial, sans-serif; color: #666666;\">"
            #add about to 3
            mail_body_4 = "</td></tr><tr><td align=\"left\" class=\"padding\" style=\"padding:0 0 45px 25px;\"><table border=\"0\" cellpadding=\"0\"cellspacing=\"0\" class=\"mobile-button-container\"><tbody><tr><td align=\"center\"><!-- BULLETPROOF BUTTON --><table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" class=\"mobile-button-container\" width=\"100%\"><tbody><tr><td align=\"center\" class=\"padding-copy\" style=\"padding: 0;\"><table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" class=\"responsive-table\"><tbody><tr><td align=\"center\"><a class=\"mobile-button\" href=\""
            #add link to 4
            mail_body_5 = "\" style=\"font-size: 15px; font-family: Helvetica, Arial, sans-serif; font-weight: normal; color: #ffffff; text-decoration: none; background-color: #256F9C; border-top: 10px solid #256F9C; border-bottom: 10px solid #256F9C; border-left: 20px solid #256F9C; border-right: 20px solid #256F9C; border-radius: 3px; -webkit-border-radius: 3px; -moz-border-radius: 3px; display: inline-block;\" target=\"_blank\">Apply Now &rarr;</a></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr>"
               
            for sc in scholarship_d:
                
                root_url = "http://scholfin.com/scholarship-details/"
                x = re.sub('[^A-Za-z0-9]+',' ',sc.name)
                x = x.strip(' ')
                x = re.sub('[^A-Za-z0-9]+','-',x)
                link = root_url + x
                am = ""
                if sc.amount == 0 :
                    am = 'Amount : Varies'
                else :
                    if sc.amount_frequency == 0 :
                        am = 'Amount : ' + str(sc.amount)
                    elif sc.amount_frequency == 1 :
                        am = 'Amount : ' + str(sc.amount) + '  Monthly'
                    else :
                        am = 'Amount : ' + str(sc.amount) + '  Yearly'

                
                t = sc.deadline.strftime("%B %d, %Y") # time of deadline of scholarship
                mail_message = mail_message + mail_body_1 + 'Deadline : ' + t + mail_body_6 + am + mail_body_2 + sc.name + mail_body_3 + sc.about + mail_body_4 + link + mail_body_5
            
        # mail_message = '<table border="2"><tr><td> asd </td> <td> dfg </td></tr> </table>'
        # mail_message = mail_body_1 + 'Deadline : ' + 't' + mail_body_6 + 'am' + mail_body_2 + 'sc.name' + mail_body_3 + 'sc.about' + mail_body_4 + 'link' + mail_body_5
        # mail_message =mail_message+ mail_body_1 + 'Deadline : ' + 't' + mail_body_6 + 'am' + mail_body_2 + 'sc.name' + mail_body_3 + 'sc.about' + mail_body_4 + 'link' + mail_body_5
        import sendgrid
        sg_username = "scholfin"
        sg_password = "sameer1234"

        sg = sendgrid.SendGridClient(sg_username, sg_password)
        message = sendgrid.Mail()

        message.set_from("thescholfin@gmail.com")
        message.set_subject("New Scholarships matching your profile !")
        if len(mail_message) == 0:
            mail_message = '<table border="2"><tr><td></td> <td></td></tr> </table>'
        message.set_html(mail_message)
        message.add_to(u.email)
        # message.add_to('palanshagarwal@gmail.com')
        # message.add_to('thescholfin@gmail.com')

        filters = {
            "templates": {
                "settings": {
                    "enable": 1,
                    "template_id": "351fd81b-d419-4d87-80ef-9de020747724"
                }
            }
        }
        for app, contents in filters.iteritems():
            for setting, value in contents['settings'].iteritems():
                message.add_filter(app, setting, value)
        try:
            status, msg = sg.send(message)
            print msg
            print count
        except:
            print 'error'
                    # pass
