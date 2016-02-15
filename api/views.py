from django.http import HttpResponse
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from models import *
from scholarships.functions import *
from scholarships.models import *
from datetime import datetime, timedelta

def getInstitutes(request):
    import json
    if request.is_ajax():
        q = request.GET.get('term', False)
        print q
        results = []
        name_json = ''
        listt = Institute.objects.filter(Q(name__istartswith=q) | Q(short_name__istartswith=q))
        for institute in listt:
            name_json = institute.name
            results.append(name_json)
        data = json.dumps(results)
        print data
    else:
        data = 'fail'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

#Helper Function to save csv data to django model
def csv_to_model(file_path):
    import csv, json
    master = {'err':[]}
    exclude_list = ['of', 'and', '&', ',', ' ', '']
    f = open(file_path, 'rt')
    count = 0
    try:
        reader = csv.reader(f)
        for row in reader:
            count += 1
            print count
            if count != 1:
                state = row[0]
                district = row[1]
                
                data = ''
                data = row[10].strip()
                if data == 'NA':
                    data = row[3]

                data = data.split(' (')[0]
                short_name = ''
                s_list = data.upper().split()
                for i in s_list:
                    # print i
                    if i.lower() not in exclude_list:
                        short_name += i[0]

                institute = Institute(name = data, short_name = short_name, state = state, district = district)
                try:
                    institute.save()
                except:
                    print 'not saved' + str(count)
                    print data
                    master['err'].append(count)
    
    finally:
        f.close()
        with open('failed.json', 'w') as f:
            json.dump(master, f, indent=4)
            f.close()

def getScholarships(request):
    import json
    if request.is_ajax():
        from scholarships.models import scholarship
        q = request.GET.get('term', False)
        print q
        results = []
        name_json = ''
        listt = scholarship.objects.filter(Q(name__istartswith=q) | Q(name__icontains=q))
        for scholarship in listt:
            name_json = scholarship.name
            results.append(name_json)
        data = json.dumps(results)
        print data
    else:
        data = 'fail'
        print data

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)



def send_intro_mail(days):
    users = User.objects.filter(date_joined__gte = datetime.now()-timedelta(days= int(days)))
    print users
    
    for user in users:
        if UserProfile.objects.filter(user = user).exists() :
            user_d = UserProfile.objects.get(user = user)
            user_table = {
                'state':user_d.user_state,
                'level':user_d.user_level,
                'religion':user_d.user_religion,
                'caste':user_d.user_caste,
                'field':user_d.user_field,
                'abroad':user_d.user_abroad,
                'gender':user_d.user_gender,

            }
            ss = []
            scholarshipss = scholarship.objects.filter(education_state__state_name=user_table['state']).filter(
                education_level__level_name=user_table['level']).filter(education_religion__religion_name=user_table['religion']).filter(
                education_caste__caste_name=user_table['caste']).filter(education_field__field_name=user_table['field'])
            for schlrshp in scholarshipss:
                if schlrshp.deadline_type == 1:
                    ss.append(schlrshp)

                elif schlrshp.deadline_type == 2:
                    ss.append(schlrshp)

            scholarships = scholarship.objects.all().filter(deadline__gte = timezone.now()).filter(education_state__state_name=user_table['state']).filter(
                education_level__level_name=user_table['level']).filter(education_religion__religion_name=user_table['religion']).filter(
                education_caste__caste_name=user_table['caste']).filter(education_field__field_name=user_table['field'])
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

            for s in ss:
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

            number_of_scholarships = 0
            amount = 0
            sctype1={}
            from django.core.exceptions import ObjectDoesNotExist
            for sc in scholarship_d:
                number_of_scholarships = number_of_scholarships + 1
                amount = amount + amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
                # sctype1[sc.scholarship_id]=sctype(sc.amount_frequency,sc.amount)
            amount = int(amount)

            amount = indianformat(amount)
            import sendgrid
            sg_username = "scholfin"
            sg_password = "sameer1234"

            sg = sendgrid.SendGridClient(sg_username, sg_password)
            message = sendgrid.Mail()
            message.set_from('thescholfin@gmail.com')
            message.set_subject('New Scholarship opportunity for you on ScholFin')
            message.set_text("This is text body")

            mail_body_3 = "</tr></td><tr><td align=\"left\" class=\"padding-copy\" style=\"padding: 10px 0 15px 25px; font-size: 16px; line-height: 24px; font-family: Helvetica, Arial, sans-serif; color: #666666;\">"

            body = '<br>Hello ' + user.first_name +',<br><br>' + ' This mail is to inform you that there are total <b>'+ str(number_of_scholarships) + ' number of scholarships worth Rs '+ str(amount) +'</b> waiting for you on your ScholFin Dashboard.<br> Click <a href="http://scholfin.com/dashboard/">here</a> to view all these scholarships where you are eligible.<br><br><h3>What is ScholFin?</h3> ScholFin is a scholarship search engine which helps students to find scholarships and education related funding where you are eligible in just 3 clicks! The total worth of scholarship on our portal is 9,458 crore which can be availed by a vast number of 10 crore students in India.<br><br>We are happy to have you as a ScholFin member and we would love to help you. in every possible way.<br>We are open to all your suggestions and feedback to serve you better.<br><br>Have a ScholFin Scholarly Education.<br>Cheers.'            
            messag = body + mail_body_3
            message.set_html(messag)
            message.add_to(user.email)
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
            status, msg = sg.send(message)
            print user

def points():
    for sch in scholarship.objects.all():
        point = float(sch.education_caste.all().count())/len(caste.objects.all())
        point += float(sch.education_interest.all().count())/len(interest.objects.all())
        point += float(sch.education_field.all().count())/len(field.objects.all())
        point += float(sch.education_religion.all().count())/len(religion.objects.all())
        point += float(sch.education_level.all().count())/len(level.objects.all())
        point += float(sch.education_state.all().count())/len(state.objects.all())
        sch.points = point + len(Provider.objects.filter(scholarship = sch)) * 100