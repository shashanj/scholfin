from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from sorting import *
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.admin.views.decorators import staff_member_required
from functions import *
from scholarships.models import *
from django.contrib.auth.hashers import make_password
from datetime import datetime,timedelta
from django.core.mail import send_mail


# Create your views here.
import re
import random, string

class Urlsetting(object):
    Queue = []

    def __init__(self,st):
        self.Queue.append(st)

    def geturl(self):
        if len(self.Queue) > 0:
            return str(self.Queue.pop())
        else :
            return '/dashboard/'

class Empty(object):
    pass

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def index(request):
    if 'userid' not in request.session:
        t = loader.get_template('scholarship/index.html')
        return HttpResponse(t.render())
    return HttpResponseRedirect('/dashboard/')


def login_page(request):
    state = 'please login ...'
    username = password = ''
    if request.POST:
        email = request.POST.get('username')
        username = email[:30]
        print username
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            if user.profile.auth_type == 'basic' or user.profile.auth_type == None:
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        request.session['userid']=user.id
                        state = "login successfull"
                        b = Empty()
                        b.__class__ = Urlsetting
                        next_url  = b.geturl()
                        return HttpResponseRedirect(next_url)
                    else:
                        state = "your account is not active"
                else:
                    state = 'your username and/or password was wrong'
            else: 
                state = 'No such user exists'
        else:
            state = 'No such user exists'
    # t=loader.get_template('scholarship/login.html');
    return render_to_response('scholarship/login.html', {'state': state, 'username': username}, RequestContext(request))

def forgot_password(request):
    state = 'Enter your email address below and we\'ll send you your new password.'
    if request.POST:
        email = request.POST.get('email')
        print email
        try:
            user = User.objects.get(email__iexact=email)
            if user.profile.auth_type == 'basic':
                subpswd1 = ''.join(random.choice(string.ascii_uppercase) for i in range(4))
                subpswd2 = ''.join(random.choice(string.digits) for i in range(4))       
                newpswd = subpswd1+subpswd2        
                
                user.set_password(newpswd)
                user.save()        

                subject = "Scholfin account new password"
                messag = "Hi "+user.first_name+", your new password for scholfin is "+newpswd;
                print messag
                import sendgrid
                sg_username = "scholfin"
                sg_password = "sameer1234"

                sg = sendgrid.SendGridClient(sg_username, sg_password)
                message = sendgrid.Mail()

                message.set_from("thescholfin@gmail.com")
                message.set_subject(subject)
                message.set_text("This is text body")
                message.set_html(messag)
                message.add_to(user.email)
                status, msg = sg.send(message)

                # send_mail(subject,message, 'info@scholfin.com', [email], fail_silently=False)
                state = 'Please check your email for the new password'
            else:
                state = 'You have registered through '+ user.profile.auth_type + 'Please use it to sign in' 
        
        except User.DoesNotExist:
            state = 'Email id entered does not exist'

        print "Email id entered does not exist"


    return render_to_response('scholarship/forgotpassword.html',{'state': state}, RequestContext(request))

@login_required(login_url='/login/')
def change_password(request):
    state = '* Please enter the new password!'
    if request.POST:
        email = request.user.email
        user = User.objects.get(email=email)
        password = request.POST.get('password')
        cp = request.POST.get('cp')
        if cp != password :
            state = "* Password didn't match"

        else:
            user.set_password(password)
            user.save() 
            state = "Password changed successfully"
            user = authenticate(username=user.username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['userid']=user.id
                    state = "login successfull"
                    return HttpResponseRedirect('/dashboard/')
                else:
                    state = "your account is not active"
            else:
                state = 'your username and/or password was wrong'

    return render_to_response('scholarship/changepassword.html',{'state': state}, RequestContext(request))


def signup(request):
    return render_to_response('scholarship/signup.html')

def fbsignup(request):
    # Settings for Facebook API call
    client_id = '1497240163926202'
    redirect_uri = 'http://www.scholfin.com/fbsignup_process/'
    scope = 'email'
    api_url = 'https://www.facebook.com/dialog/oauth?'

    return HttpResponseRedirect(api_url + 'client_id=' + client_id + '&' + 'redirect_uri=' + redirect_uri + '&' 
        + 'scope=' + scope)

@csrf_exempt
def googlesignup_process(request):
    urltogo = ''
    import requests
    # data_url = https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=youraccess_token
    auth_code = request.POST.get('codee',False)
    # print auth_code

    if auth_code:
        client_id =  '143411720163-k159r2o0uqtas51d96qqf9lri7511bjk.apps.googleusercontent.com' 
        client_secret = 'Zbgj6udZxEXiZo5I1BLiU2sA'

        redirect_uri = 'postmessage'
        data_url = 'https://www.googleapis.com/oauth2/v3/token'

        payload = {'code':auth_code, 'client_id':client_id, 'client_secret':client_secret, 'redirect_uri':redirect_uri, 'grant_type':'authorization_code' }
        r = requests.post(data_url, data=payload)

        import json
        import urllib2
        try:
            data = json.loads(r.text)
        except ValueError:
            return HttpResponseRedirect('/signup/')
        except urllib2.URLError:
            return HttpResponseRedirect('/signup/')

        access_token = data['access_token']
        # print access_token

        data_url = 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token='+access_token
            
        try:
            data = json.load(urllib2.urlopen(data_url))
        except ValueError:
            return HttpResponseRedirect('/signup/')
        except urllib2.URLError:
            return HttpResponseRedirect('/signup/')

        email = data['email']
        if len(email)>30 :
            username = email[:30]
        else :
            username = email
        print username

        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            user = None

        if user is not None:    
            userprofile = UserProfile.objects.get(user__email=email)

            if userprofile.auth_type == 'google':
                password = randomword(30)
                user.password = make_password(password=password,
                                      salt=None,
                                      hasher='unsalted_md5')
                user.save()
                user = authenticate(username=username, password=password)
                login(request,user)
                request.session['userid']=user.id
                b = Empty()
                b.__class__ = Urlsetting
                next_url  = b.geturl()
                return HttpResponseRedirect(next_url)
            else:
                error = '* This Email-id already exits Please login Normally'
                context={
                    'error' : error,
                }
                return render_to_response('scholarship/signup.html',context)

        else:
            b = Empty()
            b.__class__ = Urlsetting
            next_url  = b.geturl()
            Urlsetting(next_url)
            password = access_token
            email = data['email']
            lastname = data['family_name']
            firstname = data['given_name']
            auth_type = 'google'
            option_caste = caste.objects.all
            option_state = state.objects.all
            option_level = level.objects.all
            option_religion = religion.objects.all
            option_field = field.objects.all
            option_interest = interest.objects.all
            option_abroad = abroad.objects.all
            context_list = {'castes': option_caste,
                            'states': option_state,
                            'levels': option_level,
                            'religions': option_religion,
                            'fields': option_field,
                            'interests': option_interest,
                            'abroads': option_abroad,
                            'username': username,
                            'password': password,
                            'email': email,
                            'auth_type' : auth_type,
                            'lastname' : lastname,
                            'firstname' : firstname,
                            'next_url' : next_url,

                            }
            return render_to_response('scholarship/signup_detail.html', context_list, RequestContext(request))

    else:
        response = HttpResponseRedirect('/')

    return response


def fbsignup_process(request):
    code = request.GET.get('code', False)
    urltogo = ''
    # Settings for Facebook API call
    client_id = '1497240163926202'
    redirect_uri = 'http://www.scholfin.com/fbsignup_process/'
    api_url = 'https://graph.facebook.com/v2.3/oauth/access_token?'
    client_secret = 'c5bf6a6b7eb80fdf1326fb9112accea8'

    if code:
        import json
        import urllib2
        data_url = api_url + 'client_id=' + client_id + '&' + 'redirect_uri=' + redirect_uri + '&' + 'client_secret=' + client_secret + '&' + 'code=' + str(code)
        
        try:
            data = json.load(urllib2.urlopen(data_url))
        except ValueError:
            return HttpResponseRedirect('/')
        except urllib2.URLError:
            return HttpResponseRedirect('/')

        ##Capture access_token from JSON response
        access_token = data['access_token']

        data_url = 'https://graph.facebook.com/v2.4/me?fields=first_name,last_name,email&access_token='+access_token
        
        try:
            data = json.load(urllib2.urlopen(data_url))
        except ValueError:
            return HttpResponseRedirect('/')
        except urllib2.URLError:
            return HttpResponseRedirect('/')

        email = data['email']
        if len(email) > 30:
            username = email[:30]
        else:
            username = email
        print username

        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            user = None

        if user is not None:    
            userprofile = UserProfile.objects.get(user__email=email)

            if userprofile.auth_type == 'facebook':
                password = randomword(30)
                user.password = make_password(password=password,
                                      salt=None,
                                      hasher='unsalted_md5')
                user.save()
                user = authenticate(username=username, password=password)
                login(request,user)
                request.session['userid']=user.id
                b = Empty()
                b.__class__ = Urlsetting
                next_url  = b.geturl()
                return HttpResponseRedirect(next_url)
            else:
                error = '* This Email-id already exits Please login Normally'
                context={
                    'error' : error,
                }
                return render_to_response('scholarship/signup.html',context)
                
        else:
            b = Empty()
            b.__class__ = Urlsetting
            next_url  = b.geturl()
            Urlsetting(next_url)
            password = access_token
            email = data['email']
            lastname = data['last_name']
            firstname = data['first_name']
            auth_type = 'facebook'
            option_caste = caste.objects.all
            option_state = state.objects.all
            option_level = level.objects.all
            option_religion = religion.objects.all
            option_field = field.objects.all
            option_interest = interest.objects.all
            option_abroad = abroad.objects.all
            context_list = {'castes': option_caste,
                            'states': option_state,
                            'levels': option_level,
                            'religions': option_religion,
                            'fields': option_field,
                            'interests': option_interest,
                            'abroads': option_abroad,
                            'username': username,
                            'password': password,
                            'email': email,
                            'auth_type' : auth_type,
                            'lastname' : lastname,
                            'firstname' : firstname,
                            'next_url' : next_url,

                            }
            return render_to_response('scholarship/signup_detail.html', context_list, RequestContext(request))
        # response = HttpResponse(data.items())

    else:
        response = HttpResponseRedirect('/')

    return response

@csrf_exempt
def signup_complete(request):
    if request.POST:
        email = request.POST.get('email')
        if len(email) > 30:
            username = email[:30]
        else:
            username = email
        #print username
        password = request.POST.get('password')
        cp = request.POST.get('cp')
        print cp
        #checking username 

        #sl = User.objects.filter(username__iexact=username)
        if User.objects.filter(email__iexact=email).exists() :
            error = '* This Email-id already exits'
            context={
                'error' : error,
            }
            return render_to_response('scholarship/signup.html',context)
        #confirming password
        if cp != password :
            error = "* Password didn't match"
            email = username
            context={
                'error': error,
                'email': email,   
            }
            return render_to_response('scholarship/signup.html',context)
            
        auth_type = 'basic'
        b = Empty()
        b.__class__ = Urlsetting
        next_url  = b.geturl()
        Urlsetting(next_url)
        option_caste = caste.objects.all
        option_state = state.objects.all
        option_level = level.objects.all
        option_religion = religion.objects.all
        option_field = field.objects.all
        option_interest = interest.objects.all
        option_abroad = abroad.objects.all
        context_list = {'castes': option_caste,
                        'states': option_state,
                        'levels': option_level,
                        'religions': option_religion,
                        'fields': option_field,
                        'interests': option_interest,
                        'abroads': option_abroad,
                        'username': username,
                        'password': password,
                        'email': email,
                        'auth_type' : auth_type,
                        'next_url' : next_url,
                        }
    return render_to_response('scholarship/signup_detail.html', context_list, RequestContext(request))


def signupprocess(request):
    if request.POST:
        u_username = request.POST.get('username')
        u_email = request.POST.get('email')
        u_password = request.POST.get('password')
        u_auth_type = request.POST.get('auth_type')
        u_firstname = request.POST.get('fname')
        u_lastname = request.POST.get('lname')
        u_state = state.objects.filter(state_id=int(request.POST.get('state')))
        u_state=u_state[0]
        u_religion = religion.objects.filter(religion_id=request.POST.get('religion'))
        u_religion = u_religion[0]
        u_caste = caste.objects.filter(caste_id=request.POST.get('caste'))
        u_caste=u_caste[0]
        u_level = level.objects.filter(level_id=request.POST.get('level'))
        u_level=u_level[0]
        u_field = field.objects.filter(field_id=request.POST.get('field'))
        u_field = u_field[0]
        u_interest = request.POST.getlist('interest')
        u_gender = int(request.POST.get('gender'))
        u_study_abroad = abroad.objects.filter(abroad_id=request.POST.get('abroad'))
        u_study_abroad = u_study_abroad[0]
        u_disability = int(request.POST.get('disability'))
        u_college = request.POST.get('college')

    user_is = []
    user_is = User.objects.filter(email=u_email).count()

    if user_is is 0:
        new_user = User()
        new_user.username = u_username
        new_user.email = u_email
        new_user.first_name= u_firstname
        new_user.last_name = u_lastname
        new_user.save()
        new_user.set_password(u_password)
        new_user.save()
        print new_user
        profile = UserProfile()
        profile.user = new_user
        profile.auth_type = u_auth_type
        profile.user_state =u_state
        profile.user_religion = u_religion
        profile.user_caste = u_caste
        profile.user_field = u_field
        profile.user_gender = u_gender
        profile.user_level = u_level
        profile.user_abroad = u_study_abroad
        profile.user_disability = u_disability
        profile.user_income = u_college
        profile.save()
        for u in u_interest:
            profile.user_interest.add(u)

        user = User.objects.get(username = u_username)
        if user.profile.auth_type == 'basic' or user.profile.auth_type == None:
            user=authenticate(username=u_username, password=u_password);
            if user is not None:
                login(request,user)
                request.session['userid']=user.id
                b = Empty()
                b.__class__ = Urlsetting
                next_url  = b.geturl()
                return HttpResponseRedirect(next_url)

        elif user.profile.auth_type == 'facebook':
            password = randomword(30)
            user.password = make_password(password=password,
                                  salt=None,
                                  hasher='unsalted_md5')
            user.save()
            user = authenticate(username=u_username, password=password)
            if user is not None:
                login(request,user)
                request.session['userid']=user.id
                b = Empty()
                b.__class__ = Urlsetting
                next_url  = b.geturl()
                return HttpResponseRedirect(next_url)

        elif user.profile.auth_type == 'google':
            password = randomword(30)
            user.password = make_password(password=password,
                                  salt=None,
                                  hasher='unsalted_md5')
            user.save()
            user = authenticate(username=u_username, password=password)
            if user is not None:
                login(request,user)
                request.session['userid']=user.id
                b = Empty()
                b.__class__ = Urlsetting
                next_url  = b.geturl()
                return HttpResponseRedirect(next_url)
    return HttpResponse("error in registration")

def sort_by(request):
    pass

@login_required(login_url='/login/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    context = RequestContext(request)
    user_u = User.objects.filter(pk=request.user.id)
    user_u=user_u[0]
    user_d = UserProfile.objects.filter(user__username=request.user.username)
    user_d= user_d[0]
    # user dictionary for the searching

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
    print len(scholarship_l)
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
        try:
            temp = loggedcount.objects.get(scholarship__scholarship_id = sc.scholarship_id)
            if not temp.user.filter(username = user_u.username).exists():
                temp.user.add(user_u)
                temp.user_count = temp.user.all().count()
                temp.save()

        except ObjectDoesNotExist:
            temp = loggedcount()
            temp.scholarship = sc
            temp.save()
            temp.user.add(user_u)
            temp.user_count = temp.user.all().count()
            temp.save()
        number_of_scholarships = number_of_scholarships + 1
        amount = amount + amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
        # sctype1[sc.scholarship_id]=sctype(sc.amount_frequency,sc.amount)
        x = re.sub('[^A-Za-z0-9]+',' ',sc.name)
        x = x.strip(' ')
        x = re.sub('[^A-Za-z0-9]+','-',x)
        sc.url = x;
    amount = int(amount)
    print amount
    amount = indianformat(amount)
    # filtering out the passed deadlines
    # scholarship_d = discard_passed(scholarship_d)


    #####Sorting list on basis of deadline and amount
    sort_by = request.GET.get('sort_by',False)
    if sort_by:
        if sort_by == 'deadline_a' or sort_by == 'deadline_d':
            for_sorting = [] #deadline_type= 0&3
            year_long = [] #deadline_type= 1
            not_declared = [] #deadline_type= 2

            for schlrshp in scholarship_d:
                if schlrshp.deadline_type == 0 or schlrshp.deadline_type == 3:
                    for_sorting.append(schlrshp)

                elif schlrshp.deadline_type == 1:
                    year_long.append(schlrshp)

                else:
                    not_declared.append(schlrshp)

            if sort_by == 'deadline_a':        
                for_sorting.sort(key=lambda x: x.deadline)
                for_sorting.extend(year_long)
                for_sorting.extend(not_declared)
                context_list = {
                'scholarships': for_sorting,
                'number': number_of_scholarships,
                'amount': amount,
                'sctype1':sctype1,
                'user':user_d,
                'sorted_by':'Deadline(Ascending order)',
                }

            elif sort_by == 'deadline_d':
                for_sorting.sort(key=lambda x: x.deadline, reverse=True)
                not_declared.extend(year_long)
                not_declared.extend(for_sorting)
                context_list = {
                'scholarships': not_declared,
                'number': number_of_scholarships,
                'amount': amount,
                'sctype1':sctype1,
                'user':user_d,
                'sorted_by':'Deadline(Descending order)',
                }

        elif sort_by == 'amount_a' or sort_by == 'amount_d':
            for_sorting = []
            final_sorted = []
            for sc in scholarship_d:
                new_amount = amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
                for_sorting.append((sc, new_amount))

            if sort_by == 'amount_a':
                for_sorting.sort(key=lambda x: x[1])
                sorted_by = 'Amount(Ascending order)'

            elif sort_by == 'amount_d':
                for_sorting.sort(key=lambda x: x[1], reverse=True)
                sorted_by = 'Amount(Descending order)'

            for sc in for_sorting:
                final_sorted.append(sc[0])
                
            context_list = {
            'scholarships': final_sorted,
            'number': number_of_scholarships,
            'amount': amount,
            'sctype1':sctype1,
            'user':user_d,
            'sorted_by': sorted_by,
            }


        else:
            context_list = {
                'scholarships': scholarship_d,
                'number': number_of_scholarships,
                'amount': amount,
                'sctype1':sctype1,
                'user':user_d,
                'sorted_by': '',

            }
    else:
        context_list = {
            'scholarships': scholarship_d,
            'number': number_of_scholarships,
            'amount': amount,
            'sctype1':sctype1,
            'user':user_d,
            'sorted_by': '',

        }
    return render_to_response('scholarship/fin_dash.html', context_list, context)


def logout_user(request):
    del request.session['userid']
    logout(request)
    return render_to_response('scholarship/index.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def detail(request , scholarship_name):
    scholarshipss = 'http://www.scholfin.com/scholarship-details/' + scholarship_name + '/'
    scholarship_name = scholarship_name.replace("-","")
    i=1
    for x in scholarship.objects.all():
        s_name = re.sub('[^A-Za-z0-9]+', '', x.name)
        i=x.scholarship_id
        if s_name == scholarship_name:
            break
        
    scholarship_s = scholarship.objects.filter(pk=i)
    #scholarship_s = scholarship.objects.filter(name=scholarship_name)
    scholarship_s = scholarship_s[0]

    if 'userid' not in request.session:       
        xx = str(request.get_full_path())
        Urlsetting(xx)
    else: 
        Urlsetting('/dashboard/')
    if 'userid' not in request.session:
        userid=-1
    else:
        userid=request.session['userid']
    scholarship_s.url = scholarshipss
    return render_to_response('scholarship/details.html' , {'scholarship':scholarship_s,'userid':userid,})

@login_required(login_url='/login/')
def profilepage(request):
    option_caste = caste.objects.all
    option_state = state.objects.all
    option_level = level.objects.all
    option_religion = religion.objects.all
    option_field = field.objects.all
    option_interest = interest.objects.all
    option_abroad = abroad.objects.all
    userdetail = UserProfile.objects.get(user__email=request.user.email)
    inters =[] 
    inters = [val for val in interest.objects.all() if val in userdetail.user_interest.all()]
    op = option_interest();
    #print(userdetail.user_abroad_id)
    for i in op :
        i.bc = 0;
    for i in op : 
        for inter in inters:
            if(i == inter ):
                i.bc = 1
    context_list = {'castes': option_caste,
                    'states': option_state,
                    'levels': option_level,
                    'religions': option_religion,
                    'fields': option_field,
                    'interests': op,
                    'abroads': option_abroad,
                    'userdetail' : userdetail,
                    }
    return render_to_response('scholarship/profile.html', context_list, RequestContext(request))

@login_required(login_url='/login/')
def profilechange(request):
    if request.POST:
        u_email = request.user.email
        u_state = state.objects.filter(state_id=int(request.POST.get('state')))
        u_state=u_state[0]
        u_religion = religion.objects.filter(religion_id=request.POST.get('religion'))
        u_religion = u_religion[0]
        u_caste = caste.objects.filter(caste_id=request.POST.get('caste'))
        u_caste=u_caste[0]
        u_level = level.objects.filter(level_id=request.POST.get('level'))
        u_level=u_level[0]
        u_field = field.objects.filter(field_id=request.POST.get('field'))
        u_field = u_field[0]
        u_interest = request.POST.getlist('interest')
        u_gender = int(request.POST.get('gender'))
        u_study_abroad = abroad.objects.filter(abroad_id=request.POST.get('abroad'))
        u_study_abroad = u_study_abroad[0]
        u_disability = int(request.POST.get('disability'))

    user_is = []
    user_is = User.objects.filter(email=u_email).count()

    if user_is is 1:
        profile = UserProfile.objects.get(user__username=request.user.username)
        profile.user_state =u_state
        profile.user_religion = u_religion
        profile.user_caste = u_caste
        profile.user_field = u_field
        profile.user_gender = u_gender
        profile.user_level = u_level
        profile.user_abroad = u_study_abroad
        profile.user_disability = u_disability
        profile_interest = interest.objects.filter(userprofile=profile)
        profile.save()
        for u in profile_interest:
            profile.user_interest.remove(u)
        profile.save()
        for u in u_interest:
            profile.user_interest.add(u)
        profile.save()
    return HttpResponseRedirect('/dashboard/')

def contact_us(request):
    if 'userid' not in request.session:
        userid=-1
    else:
        userid=request.session['userid']
    context = {
        'userid' :  userid,
    } 
    if request.POST:
        subject = request.POST.get('subject')
        uid = request.POST.get('email_id')
        phno = request.POST.get('phone')
        mess = request.POST.get('message')
        if subject is None :
            subject = 'Query contact us page'
        try :
            send_mail(subject, mess, uid,
                    ['thescholfin@gmail.com', 'shubham.879@gmail.com','info@scholfin.com'],fail_silently=True)
            context['mes'] = "Thank you for contacting us. We will reply as soon as possible."
            
        except BadHeaderError:
            context['mes'] = "Something Went wrong"
            return HttpResponse('Invalid header found.')
    

    return render_to_response('scholarship/contact_us.html',context,RequestContext(request))

def about_us(request) :
    if 'userid' not in request.session:
        userid=-1
    else:
        userid=request.session['userid']
    context = {
        'userid' :  userid,
    }
    return render_to_response('scholarship/about_us.html',context)

@login_required(login_url='/login/')
def old_scholarship(request):
    context = RequestContext(request)
    user_u = User.objects.filter(pk=request.user.id)
    user_u=user_u[0]
    user_d = UserProfile.objects.filter(user__username=request.user.username)
    user_d= user_d[0]
    # user dictionary for the searching

    user_table = {
        'state':user_d.user_state,
        'level':user_d.user_level,
        'religion':user_d.user_religion,
        'caste':user_d.user_caste,
        'field':user_d.user_field,
        'abroad':user_d.user_abroad,
        'gender':user_d.user_gender,

    }
    scholarships = scholarship.objects.all().filter(deadline_type = 0 ).filter(deadline__lt = timezone.now()).filter(education_state__state_name=user_table['state']).filter(
        education_level__level_name=user_table['level']).filter(education_religion__religion_name=user_table['religion']).filter(
        education_caste__caste_name=user_table['caste']).filter(education_field__field_name=user_table['field']) | scholarship.objects.all().filter(deadline_type =3).filter(deadline__lt = timezone.now()).filter(education_state__state_name=user_table['state']).filter(
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
    print len(scholarship_l)
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




    print 'hi'
    print len(scholarship_d)
    number_of_scholarships = 0
    amount = 0
    sctype1={}
    for sc in scholarship_d:
        number_of_scholarships = number_of_scholarships + 1
        amount = amount + amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
        # sctype1[sc.scholarship_id]=sctype(sc.amount_frequency,sc.amount)
        x = re.sub('[^A-Za-z0-9]+',' ',sc.name)
        x = x.strip(' ')
        x = re.sub('[^A-Za-z0-9]+','-',x)
        sc.url = x;
    amount = int(amount)
    print amount
    amount = indianformat(amount)
    # filtering out the passed deadlines
    # scholarship_d = discard_passed(scholarship_d)


    #####Sorting list on basis of deadline and amount
    sort_by = request.GET.get('sort_by',False)
    if sort_by:
        if sort_by == 'deadline_a' or sort_by == 'deadline_d':
            for_sorting = [] #deadline_type= 0&3
            year_long = [] #deadline_type= 1
            not_declared = [] #deadline_type= 2

            for schlrshp in scholarship_d:
                if schlrshp.deadline_type == 0 or schlrshp.deadline_type == 3:
                    for_sorting.append(schlrshp)


            if sort_by == 'deadline_a':        
                for_sorting.sort(key=lambda x: x.deadline)
                for_sorting.extend(year_long)
                for_sorting.extend(not_declared)
                context_list = {
                'scholarships': for_sorting,
                'number': number_of_scholarships,
                'amount': amount,
                'sctype1':sctype1,
                'user':user_d,
                'sorted_by':'Deadline(Ascending order)',
                }

            elif sort_by == 'deadline_d':
                for_sorting.sort(key=lambda x: x.deadline, reverse=True)
                not_declared.extend(year_long)
                not_declared.extend(for_sorting)
                context_list = {
                'scholarships': not_declared,
                'number': number_of_scholarships,
                'amount': amount,
                'sctype1':sctype1,
                'user':user_d,
                'sorted_by':'Deadline(Descending order)',
                }

        elif sort_by == 'amount_a' or sort_by == 'amount_d':
            for_sorting = []
            final_sorted = []
            for sc in scholarship_d:
                new_amount = amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
                for_sorting.append((sc, new_amount))

            if sort_by == 'amount_a':
                for_sorting.sort(key=lambda x: x[1])
                sorted_by = 'Amount(Ascending order)'

            elif sort_by == 'amount_d':
                for_sorting.sort(key=lambda x: x[1], reverse=True)
                sorted_by = 'Amount(Descending order)'

            for sc in for_sorting:
                final_sorted.append(sc[0])
                
            context_list = {
            'scholarships': final_sorted,
            'number': number_of_scholarships,
            'amount': amount,
            'sctype1':sctype1,
            'user':user_d,
            'sorted_by': sorted_by,
            }


        else:
            context_list = {
                'scholarships': scholarship_d,
                'number': number_of_scholarships,
                'amount': amount,
                'sctype1':sctype1,
                'user':user_d,
                'sorted_by': '',

            }
    else:
        context_list = {
            'scholarships': scholarship_d,
            'number': number_of_scholarships,
            'amount': amount,
            'sctype1':sctype1,
            'user':user_d,
            'sorted_by': '',

        }
    return render_to_response('scholarship/fin_dash.html', context_list, context)

def internship(request):
    return HttpResponseRedirect('https://docs.google.com/forms/d/1ON0e_gzn4wUtd21my4axak04ozQ7H8Ko24ucZzA9Ojw/viewform')

@login_required(login_url='/login/')
def apply_aa(request):
    return render_to_response('scholarship/vnitaa.html',RequestContext(request))
@csrf_exempt
def resetnexturl(request):
    if request.POST:
        Urlsetting('/dashboard/')
        return HttpResponse(200)