from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.views.decorators.cache import cache_control

from scholarships.models import *
import re
from datetime import datetime,timedelta
from django.core.mail import send_mail

from forms import ScholarshipForm

@staff_member_required
def index(request):
    context = RequestContext(request)
    page_title = 'Dashboard'
    context_list = {
            'dashboard': True,
            'page_title' : page_title,
            }
    return render_to_response('custom_admin/index.html',context_list,context)

@staff_member_required
def all_scholarship(request):
    context = RequestContext(request)
    page_title = 'All the scholarships'
    scholarships = scholarship.objects.all()

    context_list = {
            'scholarships': scholarships,
            'page_title' : page_title,
            }
    return render_to_response('custom_admin/index.html',context_list,context)

@staff_member_required
def deadline_crossed(request):
    context = RequestContext(request)
    page_title = ' The scholarships whose deadline have crossed (expired ones)'
    scholarships = scholarship.objects.filter(deadline_type = 0 ).filter(deadline__lt = timezone.now())

    context_list = {
            'scholarships': scholarships,
            'page_title' : page_title,
            }
    return render_to_response('custom_admin/index.html',context_list,context)

@staff_member_required
def deadline_open(request):
    context = RequestContext(request)
    page_title = ' The scholarships whose deadline are open (open ones)'
    scholarships = scholarship.objects.filter(deadline_type = 0 ).filter(deadline__gte = timezone.now())

    context_list = {
            'scholarships': scholarships,
            'page_title' : page_title,
            }
    return render_to_response('custom_admin/index.html',context_list,context)

@staff_member_required
def deadline_launch_and_closed(request):
    context = RequestContext(request)
    page_title = ' The scholarships that are launched and close'
    scholarships = scholarship.objects.filter(deadline_type__gte = 100 )

    context_list = {
            'scholarships': scholarships,
            'page_title' : page_title,
            }
    return render_to_response('custom_admin/index.html',context_list,context)

@staff_member_required
def deadline_type_1(request):
    context = RequestContext(request)
    page_title = ' The Scholarships whose deadline type is 1'
    scholarships = scholarship.objects.filter(deadline_type = 1 )

    context_list = {
            'scholarships': scholarships,
            'page_title' : page_title,
            }
    return render_to_response('custom_admin/index.html',context_list,context)

@staff_member_required
def deadline_type_2(request):
    context = RequestContext(request)
    page_title = ' The Scholarships whose deadline type is 2'
    scholarships = scholarship.objects.filter(deadline_type = 2 )

    context_list = {
            'scholarships': scholarships,
            'page_title' : page_title,
            }
    return render_to_response('custom_admin/index.html',context_list,context)

@staff_member_required
def deadline_type_3(request):
    context = RequestContext(request)
    page_title = ' The Scholarships whose deadline type is 3'
    scholarships = scholarship.objects.filter(deadline_type = 3 )

    context_list = {
            'scholarships': scholarships,
            'page_title' : page_title,
            }
    return render_to_response('custom_admin/index.html',context_list,context)

@staff_member_required
def amount_equal_0(request):
    context = RequestContext(request)
    page_title = ' The Scholarships whose amount is equal to 0 or left blank'
    scholarships = scholarship.objects.filter(Q(amount=0) | Q(amount=None))

    context_list = {
            'scholarships': scholarships,
            'page_title' : page_title,
            }
    return render_to_response('custom_admin/index.html',context_list,context)


@staff_member_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def weekly_update(request):
    context = RequestContext(request)
    total_users = User.objects.count()
    # total_users = 500
    context_list = {
            'total_users': total_users,
            'message':'',
            }
    return render_to_response('custom_admin/weekly_update.html',context_list,context)



@staff_member_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def send_weekly_update(request):
    context = RequestContext(request)
    if request.method == 'POST':
        lower_bound = int(request.POST.get('lower_bound',False))
        upper_bound = int(request.POST.get('upper_bound', False))

        total_users = User.objects.count()
        # total_users = 500
        if not upper_bound < total_users:
            upper_bound = total_users
        user = User.objects.all().order_by('id')[lower_bound-1:upper_bound]
        count = 0
        for u in user:
            count+=1
            if u.is_superuser==0 or u.is_staff==0:
                print u.email
                print u.username
                
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
                       
                    mail_message = ""


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
        context_list = {
            'total_users': total_users,
            'message':'email has been sent to users from '+ str(lower_bound)+ ' to ' + str(upper_bound),
            }
        return render_to_response('custom_admin/weekly_update.html',context_list,context)
    return HttpResponseRedirect('/a78shfbwifhbiwh324b2r2kjvr3h4brl3hb4r13hbrl/custom_admin/')


@staff_member_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def scholarship_diff(request):
    context = RequestContext(request)
    total_schols = scholarship.objects.count()
    # total_users = 500
    context_list = {
            'total_schols': total_schols,
            'message':'',
            }
    return render_to_response('custom_admin/scholarship_diff.html',context_list,context)


@staff_member_required
def cal_scholarship_diff(request):
    import urllib2
    context = RequestContext(request)
    if request.method == 'POST':
        lower_bound = int(request.POST.get('lower_bound',False))
        upper_bound = int(request.POST.get('upper_bound', False))

        total_schols = scholarship.objects.count()
        print total_schols
        # total_users = 500
        if not upper_bound < total_schols:
            upper_bound = total_schols
        
        count = 0
        page_title = ' The Scholarships whose page source has been changed'
        sources = page_source.objects.select_related('scholarship').all().order_by('scholarship_id')[lower_bound-1:upper_bound]
        print sources
        source_schol = [x.scholarship for x in sources]
        scholarships = scholarship.objects.all().order_by('scholarship_id')[lower_bound-1:upper_bound]
        print scholarships
        scholarship_d = []
        for s in scholarships:
            print 'opo'
            if s in source_schol:
                print s
                try:
                    response = urllib2.urlopen(s.apply_link)
                    print s.apply_link
                    p_source = response.read()
                    print 'bef'
                    # print str(p_source)
                    print type(p_source) 
                    print type(s.page_source.source)
                    if not p_source.decode('utf-8') == s.page_source.source:
                        print 'aft'
                        scholarship_d.append(s)
                except:
                    pass
            else:
                try:
                    response = urllib2.urlopen(s.apply_link)
                    p_source = response.read()
                    print p_source
                    temp = page_source()
                    temp.source = p_source
                    temp.scholarship = s
                    temp.save()
                except:
                    pass

        # print scholarship_d
        context_list = {
                'scholarships' : scholarship_d,
                'total_schols': total_schols,
                'message':'Scholarships between ' + str(lower_bound) + ' to ' +str(upper_bound)
                + ' whose source is changed are: ',
                }
        return render_to_response('custom_admin/scholarship_diff.html',context_list,context)

    return HttpResponseRedirect('/a78shfbwifhbiwh324b2r2kjvr3h4brl3hb4r13hbrl/custom_admin/')

@staff_member_required
def update_scholarship_source(request):
    import urllib2
    context = RequestContext(request)
    if request.method == 'POST':
        inp = request.POST.get('id',False)
        if inp:
            p = page_source.objects.filter(scholarship__scholarship_id = inp)
            response = urllib2.urlopen(p[0].scholarship.apply_link)
            p_source = response.read()
            p[0].source = p_source 
            p[0].save
        else:
            return HttpResponse('error text box empty')  
    else:
        return render_to_response('custom_admin/scholarship_diff.html', context )

@staff_member_required
def add_scholarship(request):
    context = RequestContext(request)
    form = ScholarshipForm(request.POST or None, initial={'display_income': 'Test'})
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/a78shfbwifhbiwh324b2r2kjvr3h4brl3hb4r13hbrl/custom_admin/scholarships/view/')
    data = {'form': form}
    return render_to_response('custom_admin/add_scholarship.html', data, context )

@staff_member_required
def view_scholarships(request):
    context = RequestContext(request)
    scholarships = scholarship.objects.all()
    context_list = {
            'scholarships': scholarships,
            }
    return render_to_response('custom_admin/view_scholarships.html',context_list,context)

@staff_member_required
def edit_scholarship(request, scholarship_id):
    from django.shortcuts import get_object_or_404
    context = RequestContext(request)
    instance = get_object_or_404(scholarship, scholarship_id=scholarship_id)
    form = ScholarshipForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/a78shfbwifhbiwh324b2r2kjvr3h4brl3hb4r13hbrl/custom_admin/scholarships/view/')
    data = {'form': form}
    return render_to_response('custom_admin/add_scholarship.html', data, context )