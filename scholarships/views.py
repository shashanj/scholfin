from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from sorting import *
from django.contrib.auth.models import User

from functions import *
from scholarships.models import *


# Create your views here.

def index(request):
	if 'userid' not in request.session:
		t = loader.get_template('scholarship/index.html')
		return HttpResponse(t.render())
	return HttpResponseRedirect('/dashboard/')


def login_page(request):
    state = 'please login ...'
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        print username
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
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
    # t=loader.get_template('scholarship/login.html');
    return render_to_response('scholarship/login.html', {'state': state, 'username': username}, RequestContext(request))


def forgot_password(request):
    if request.POST:
        email = request.POST.get('email')

    return render_to_response('scholarship/forgotpassword.html')


def signup(request):
    return render_to_response('scholarship/signup.html')


@csrf_exempt
def signup_complete(request):
    if request.POST:
        username = request.POST.get('email')
        email = username
        #print username
        password = request.POST.get('password')
        cp = request.POST.get('cp')

        #checking username 

        #sl = User.objects.filter(username__iexact=username)
        if User.objects.filter(username__iexact=username).exists() :
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
                        }
    return render_to_response('scholarship/signup_detail.html', context_list, RequestContext(request))


def signupprocess(request):
    if request.POST:
        u_username = request.POST.get('username')
        u_email = request.POST.get('email')
        u_password = request.POST.get('password')
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
        profile.user_state =u_state
        profile.user_religion = u_religion
        profile.user_caste = u_caste
        profile.user_field = u_field
        profile.user_gender = u_gender
        profile.user_level = u_level
        profile.user_abroad = u_study_abroad
        profile.user_disability = u_disability
        profile.save()
        for u in u_interest:
            profile.user_interest.add(u)
        profile.save()
        user=authenticate(username=u_username, password=u_password);
        if user is not None:
            login(request,user)
            request.session['userid']=user.id
            return HttpResponseRedirect('/dashboard/')
    return HttpResponse("error in registration")


@login_required(login_url='/login/')
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
    scholarships = scholarship.objects.filter(education_state__state_name=user_table['state']).filter(
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

    number_of_scholarships = 0
    amount = 0
    sctype1={}
    for sc in scholarship_d:
        number_of_scholarships = number_of_scholarships + 1
        amount = amount + amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
        sctype1[sc.scholarship_id]=sctype(sc.amount_frequency,sc.amount)
    amount = int(amount)
    print amount
    amount = indianformat(amount)
    context_list = {
        'scholarships': scholarship_d,
        'number': number_of_scholarships,
        'amount': amount,
        'sctype1':sctype1,
        'user':user_d,

    }
    return render_to_response('scholarship/fin_dash.html', context_list, context)


def logout_user(request):
	del request.session['userid']
	logout(request)
	return render_to_response('scholarship/index.html')


def detail(request , scholarship_name):
    scholarship_s = scholarship.objects.filter(name=scholarship_name)
    scholarship_s=scholarship_s[0]
    if 'userid' not in request.session:
    	userid=-1
    else:
    	userid=request.session['userid']
    
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
    context_list = {'castes': option_caste,
                    'states': option_state,
                    'levels': option_level,
                    'religions': option_religion,
                    'fields': option_field,
                    'interests': option_interest,
                    'abroads': option_abroad,
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
