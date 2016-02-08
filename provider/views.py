from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.admin.views.decorators import staff_member_required
from scholarships.models import *
from django.contrib.auth.hashers import make_password
from datetime import datetime,timedelta
from django.core import serializers
from django.core.mail import send_mail
import re
import random, string


def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

# Create your views here.
def index(request):
    if 'userid' not in request.session:
        t = loader.get_template('provider/index.html')
        return HttpResponse(t.render())
    else:
        return HttpResponseRedirect('/provider/dashboard/')

def login_user(request):
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
            try :
                userprofile = UserProfile.objects.get(user__email=email)
                state = 'this account is Registered for student'
            except UserProfile.DoesNotExist:
                provider = Provider.objects.get(user__email = email)
                if provider.auth_type == 'basic':
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            request.session['userid']=user.id
                            state = "login successfull"
                            return HttpResponseRedirect('/provider/dashboard/')
                        else:
                            state = "your account is not active"
                    else:
                        state = 'your username and/or password was wrong'
                else:
                    state = 'try login with ' + str(provider.auth_type)    	
        else:
            state = 'No such user exists'
    return render_to_response('provider/login.html', {'state': state, 'username': username}, RequestContext(request))

def signup(request):
    if request.POST:
        email = request.POST.get('email')
        if len(email) > 30:
            username = email[:30]
        else:
            username = email

        password = request.POST.get('password')
        cp = request.POST.get('cp')

        if User.objects.filter(email__iexact=email).exists() :
            error = '* This Email-id already exits'
            context={
                'error' : error,
            }
            return render_to_response('provider/signup.html',context,RequestContext(request))
        #confirming password
        if UserProfile.objects.filter(user__email__iexact=email).exists() :
            error = '* This Email-id already exits as a student'
            context={
                'error' : error,
            }
            return render_to_response('provider/signup.html',context,RequestContext(request))
        if cp != password :
            error = "* Password didn't match"
            email = username
            context={
                'error': error,
                'email': email,   
            }
            return render_to_response('provider/signup.html',context,RequestContext(request))
        new_user = User.objects.create_user(username,email,password)
    	new_user.save()
    	provider = Provider()
    	provider.user = new_user
    	provider.auth_type = 'basic'
    	provider.save()
        user = authenticate(username= username, password= password)
        if user is not None:
            login(request,user)
            request.session['userid']=user.id
            return HttpResponseRedirect('/provider/dashboard/')
    else:
        return render_to_response('provider/signup.html',RequestContext(request))

def fbsignup(request):
    # Settings for Facebook API call
    client_id = '1497240163926202'
    redirect_uri = 'http://www.scholfin.com/provider/fbsignup_process/'
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
            return HttpResponseRedirect('provider/signup/')
        except urllib2.URLError:
            return HttpResponseRedirect('provider/signup/')

        access_token = data['access_token']
        # print access_token

        data_url = 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token='+access_token
            
        try:
            data = json.load(urllib2.urlopen(data_url))
        except ValueError:
            return HttpResponseRedirect('provider/signup/')
        except urllib2.URLError:
            return HttpResponseRedirect('provider/signup/')

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
            try :
                userprofile = UserProfile.objects.get(user__email=email)
                error = '* Register with differnt Email-id this is used for student account'
                context = {
                    'error' : error,
                }
                return render_to_response('provider/signup.html',context)
            except :
                provider = Provider.objects.get(user__email=email)
                if userprofile is None :
                    if provider.auth_type == 'google':
    	                password = randomword(30)
    	                user.password = make_password(password=password,
    	                                      salt=None,
    	                                      hasher='unsalted_md5')
    	                user.save()
    	                user = authenticate(username=username, password=password)
    	                login(request,user)
    	                request.session['userid']=user.id
    	                return HttpResponseRedirect('/provider/dashboard/')
                    else:
    	                error = '* This Email-id already exits Please login Normally'
    	                context={
    	                    'error' : error,
    	                }
    	                return render_to_response('provider/signup.html',context)  
        else:
            password = randomword(30)
            new_user = User.objects.create_user(username,email,make_password(password=password,
                                  salt=None,
                                  hasher='unsalted_md5'))
            new_user.save()
            provider = Provider()
            provider.user = new_user
            provider.auth_type = 'google'
            provider.save()
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                request.session['userid']=user.id
                return HttpResponseRedirect('/provider/dashboard/')

    else:
        response = HttpResponseRedirect('/provider/')

    return response

def fbsignup_process(request):
    code = request.GET.get('code', False)
    urltogo = ''
    # Settings for Facebook API call
    client_id = '1497240163926202'
    redirect_uri = 'http://www.scholfin.com/provider/fbsignup_process/'
    api_url = 'https://graph.facebook.com/v2.3/oauth/access_token?'
    client_secret = 'c5bf6a6b7eb80fdf1326fb9112accea8'

    if code:
        import json
        import urllib2
        data_url = api_url + 'client_id=' + client_id + '&' + 'redirect_uri=' + redirect_uri + '&' + 'client_secret=' + client_secret + '&' + 'code=' + str(code)
        
        try:
            data = json.load(urllib2.urlopen(data_url))
        except ValueError:
            return HttpResponseRedirect('`/provider/')
        except urllib2.URLError:
            return HttpResponseRedirect('`/provider/')

        ##Capture access_token from JSON response
        access_token = data['access_token']

        data_url = 'https://graph.facebook.com/v2.4/me?fields=first_name,last_name,email&access_token='+access_token
        
        try:
            data = json.load(urllib2.urlopen(data_url))
        except ValueError:
            return HttpResponseRedirect('`/provider/')
        except urllib2.URLError:
            return HttpResponseRedirect('`/provider/')

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
            try :
                userprofile = UserProfile.objects.get(user__email=email)
                error = '* Register with differnt Email-id this is used for student account'
                context={
                    'error' : error,
                }
                return render_to_response('provider/signup.html',context)
            
            except:
                provider = Provider.objects.get(user__email=email)
                if provider.auth_type == 'facebook':
                    password = randomword(30)
                    user.password = make_password(password=password,
                                          salt=None,
                                          hasher='unsalted_md5')
                    user.save()
                    user = authenticate(username=username, password=password)
                    login(request,user)
                    request.session['userid']=user.id
                    return HttpResponseRedirect('/provider/dashboard/')
                else:
                    error = '* This Email-id already exits Please login Normally'
                    context={
                        'error' : error,
                    }
                    return render_to_response('provider/signup.html',context)
                
        else:
            password = randomword(30)
            new_user = User.objects.create_user(username,email,make_password(password=password,
                                  salt=None,
                                  hasher='unsalted_md5'))
            new_user.save()
            provider = Provider()
            provider.user = new_user
            provider.auth_type = 'facebook'
            provider.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                request.session['userid']=user.id
                return HttpResponseRedirect('/provider/dashboard/')

    else:
        response = HttpResponseRedirect('/provider/')

    return response

def logout_user(request):
    del request.session['userid']
    logout(request)
    return HttpResponseRedirect('/provider/')

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
                    return HttpResponseRedirect('/provider/dashboard/')
                else:
                    state = "your account is not active"
            else:
                state = 'your username and/or password was wrong'

    return render_to_response('provider/changepassword.html',{'state': state}, RequestContext(request))


@login_required(login_url='/provider/login/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    userid=request.session['userid']
    user = User.objects.get(id=userid)
    provider = Provider.objects.get(user__id = userid)
    pro_schol = provider.scholarship.all()
    for sch in pro_schol:
        x = re.sub('[^A-Za-z0-9]+',' ',sch.name)
        x = x.strip(' ')
        x = re.sub('[^A-Za-z0-9]+','-',x)
        sch.url = x
        date = str(sch.deadline - timezone.now())
        date = date[:date.find('days')+4]
        l1=len(date)
        date = re.sub('-', '',date)
        l1=l1-len(date)
        if l1 == 0:
            sch.status = 'live'
        else :
            sch.status = 'dead'
        app = Applicant.objects.filter(scholarship = sch)
        if len(app) > 0:
            app = len(app[0].applicant.all())
        else :
            app = 0
        sch.app = app
    context={
        'scholarship':pro_schol,
        'pro' : User.objects.get(id = request.session['userid']),
    }
    return render_to_response('provider/list.html',context,RequestContext(request))

@login_required(login_url='/provider/login/')
def details(request, scholarship_name):
    state = ''
    url = scholarship_name
    scholarship_name = scholarship_name.replace("-","")
    i=1
    for x in scholarship.objects.all():
        s_name = re.sub('[^A-Za-z0-9]+', '', x.name)
        i=x.scholarship_id
        if s_name == scholarship_name:
            break
    # scholrship name    
    scholarship_s = scholarship.objects.filter(pk=i)
    scholarship_s = scholarship_s[0]
    #deadline
    date = str(scholarship_s.deadline - timezone.now())
    date = date[:date.find('days')+4]
    l1=len(date)
    date = re.sub('-', '',date)
    l1=l1-len(date)

    # dashboard views
    dash = loggedcount.objects.filter(scholarship = scholarship_s)
    if len(dash) > 0:
        dash = dash[0].user_count
    else:
        dash = 0

    # page views
    view = scholarship_s.organic_view + scholarship_s.logged_view

    # applied
    app = Applicant.objects.filter(scholarship = scholarship_s)
    if len(app) > 0:
        app = len(app[0].applicant.all())
    else :
        app = 0
    # clicks
    click = scholarship_s.apply_click
    if request.method == 'POST':
        u = request.POST.get('members').split(';')
        u = User.objects.filter(email__in = u)
        if len(u) ==0 :
            import sendgrid
            sg_username = "scholfin"
            sg_password = "sameer1234"

            sg = sendgrid.SendGridClient(sg_username, sg_password)
            message = sendgrid.Mail()
            subject = 'Invitation to join '+ scholarship_s.name + ' as admin'
            message.set_from("thescholfin@gmail.com")
            message.set_subject(subject)
            message.set_text("This is text body")
            use = User.objects.get(id=request.session['userid']).first_name
            messag = 'Hi, ' + use + 'has invited you to in join the administration of '+ scholarship_s.name + '. Your Password is 12345678'
            if request.POST.get('mess') is not None:
                messag = messag + use + ' sends you this message - ' + request.POST.get('mess') + 'Thanks Scholfin'
            message.set_html(messag)
            emaily = request.POST.get('members').split(';')
            for x in emaily:
                message.add_to(x)
                users = User.objects.filter(email = x)
                if len(users) ==  0:
                    new = User.objects.create_user(x[:30],x,'12345678')
                    new.save()
                    pro = Provider()
                    pro.user = new
                    pro.auth_type = 'basic'
                    pro.save()
                    pro.scholarship.add(scholarship_s)
                    pro.save()
                else:
                    users = users[0]
                    provider = Provider.objects.filter(user = users)
                    if len(provider) == 0:
                        pro = Provider()
                        pro.user = users
                        pro.auth_type = 'basic'
                        pro.save()
                        pro.scholarship.add(scholarship_s)
                        pro.save()
                    else:
                        provider = provider[0]
                        provider.scholarship.add(scholarship_s)
                        provider.save()
                state = 'Members have been successfully invited'
            try:
                status, msg = sg.send(message)
            except : 
                print 'error in sending email'
        else:
            state=''

    context = {
    'scholarship' : scholarship_s,
    'dash' : dash,
    'date' : date,
    'status' : l1,
    'view' : view,
    'app' : app,
    'click' : click,
    'url' : url,
    'state' : state,
    'pro' : User.objects.get(id = request.session['userid'])
    }
    return render_to_response('provider/dashboard.html',context,RequestContext(request))

@csrf_exempt
@login_required(login_url='/provider/login/')
def getactivity(request):
    if request.is_ajax:
        if request.method == 'POST':
            activitys = []
            scholarship_name = request.POST.get('val').replace("-","")
            i=1
            for x in scholarship.objects.all():
                s_name = re.sub('[^A-Za-z0-9]+', '', x.name)
                i=x.scholarship_id
                if s_name == scholarship_name:
                    break
            # scholrship name    
            scholarship_s = scholarship.objects.filter(pk=i)
            sch = scholarship_s[0]
            import json,time
            act = activity.objects.filter(scholarship__name=sch).order_by('-timestamp')[:4]

            for x in act:
                ti = (x.timestamp).strftime('%Y/%m/%d %H:%M')
                activitys.append({'act' : str(x.user.first_name+' ' + x.user.last_name + x.activity + ' on ' + ti)})

            return HttpResponse(json.dumps(activitys))

@login_required(login_url='/provider/login/')
def response(request,scholarship_name):
    url = scholarship_name
    scholarship_name = scholarship_name.replace("-","")
    i=1
    for x in scholarship.objects.all():
        s_name = re.sub('[^A-Za-z0-9]+', '', x.name)
        i=x.scholarship_id
        if s_name == scholarship_name:
            break   
    scholarship_s = scholarship.objects.filter(pk=i)
    scholarship_s = scholarship_s[0]

    app = Applicant.objects.filter(scholarship = scholarship_s).values('applicant')
    prof = UserProfile.objects.filter(user__in = app)
    ques = question.objects.filter(scholarship = scholarship_s)
    notes = Note.objects.filter(scholarship = scholarship_s).filter(by__id = request.session['userid'])
    for  usr in prof :
        ans  = answer.objects.filter(user = usr.user).filter(question__scholarship = scholarship_s)
        usr.answ = ans
        try:
            usr.notes = notes.get(of = usr.user).note
        except:
            usr.notes = ''
        if Selected.objects.filter(scholarship = scholarship_s).filter(selected__id = usr.user.id).exists():
            usr.level = 'selected'
        elif ShortList.objects.filter(scholarship = scholarship_s).filter(shortlist__id = usr.user.id).exists():
            usr.level = 'shortlisted'
        elif Rejected.objects.filter(scholarship = scholarship_s).filter(rejected__id = usr.user.id).exists():
            usr.level = 'rejected'
        else:
            usr.level = 'not decided yet'

    doclist = document.objects.filter(scholarship = scholarship_s)
    for  usr in prof :
        usr.docs = UserDocuments.objects.filter(user = usr).filter(docs__in= doclist)
        

    context = {
        'scholarship' : scholarship_s,
        'prof' : prof,
        'url' : url,
        'pro' : User.objects.get(id = request.session['userid']),
    }
    
    return render_to_response('provider/response.html',context,RequestContext(request))

@login_required(login_url='/provider/login/')
def action(request):
    if request.POST:
        app = request.POST.get('applicant')
        sch = request.POST.get('scholarship')
        url = request.POST.get('url')
        scholarship_s = scholarship.objects.get(name = sch)
        app = User.objects.get(email = app)
        action = request.POST.get('action')
        ###################################################################
        if action == 'shortlist' :            
            try:
                shr = ShortList.objects.get(scholarship =  scholarship_s)
                shr.shortlist.add(app)
                shr.count = shr.count+1
                shr.save()
            except ShortList.DoesNotExist:
                shr = ShortList()
                shr.scholarship = scholarship_s
                shr.save()
                shr.shortlist.add(app)
                shr.count = 1
                shr.save()
            try:
                shr = Rejected.objects.get(scholarship =  scholarship_s)
                try:
                    print 'ihi'
                    shr.rejected.remove(app)
                    shr.count = shr.count - 1
                    shr.save()
                except:
                    pass
            except:
                pass

            import sendgrid
            sg_username = "scholfin"
            sg_password = "sameer1234"

            sg = sendgrid.SendGridClient(sg_username, sg_password)
            message = sendgrid.Mail()
            subject = request.POST.get('sub')
            message.set_from("thescholfin@gmail.com")
            message.set_subject('Congrats You ave been Shortlisted')
            message.set_text("This is text body")
            body = 'hi ' + app.first_name + ', You have been shortlisted for' + sch + ' For further process contact the scholarship provider'
            messag = body
            message.set_html(messag)
            shr = ShortList.objects.filter(scholarship = scholarship_s)[0]
            message.add_to(app.email)
            message.add_to('thescholfin@gmail.com')
            status, msg = sg.send(message)

            
            state = app.first_name + ' has been shortlisted'
            active = 1
        ####################################################################
        elif action == 'reject':
            state = app.first_name + ' has been rejected'
            active = 1
            try:
                rej = Rejected.objects.get(scholarship =  scholarship_s)
                rej.rejected.add(app)
                rej.count = rej.count+1
                rej.save()
            except Rejected.DoesNotExist:
                rej = Rejected()
                rej.scholarship = scholarship_s
                rej.save()
                rej.rejected.add(app)
                rej.count = 1
                rej.save()
            try:
                shr = ShortList.objects.get(scholarship =  scholarship_s)
                try:
                    print 'ihi'
                    shr.shortlist.remove(app)
                    shr.count = shr.count - 1
                    shr.save()
                except:
                    pass
            except:
                pass
            try:
                shr = Selected.objects.get(scholarship =  scholarship_s)
                try:
                    shr.selected.remove(app)
                    shr.count = shr.count - 1
                    shr.save()
                except:
                    pass
            except:
                pass
        ####################################################################
        elif action == 'mail':
            body = request.POST.get('mess')
            import sendgrid
            sg_username = "scholfin"
            sg_password = "sameer1234"

            sg = sendgrid.SendGridClient(sg_username, sg_password)
            message = sendgrid.Mail()
            subject = request.POST.get('sub')
            message.set_from((User.objects.get(id = request.session['userid'])).email)
            message.set_subject(subject)
            message.set_text("This is text body")
            messag = body
            message.set_html(messag)
            message.add_to(app.email)
            message.add_to('thescholfin@gmail.com')
            status, msg = sg.send(message)

            state = 'email has been sent'
            active = 2
        ####################################################################
        elif action == 'savenote':
            notes = request.POST.get('notes')
            by = (User.objects.get(id = request.session['userid']))
            nt = Note.objects.filter(scholarship = scholarship_s).filter(by = by).filter(of = app)
            if len(nt) == 0 :
                new_note = Note()
                new_note.scholarship = scholarship_s
                new_note.by = by
                new_note.of = app
                new_note.note = notes
                new_note.save()
            else:
                nt = nt[0]
                nt.note = notes
                nt.save()
            state = ' note saved'
            active = 3
        ####################################################################
        elif action == 'deletenote':
            by = (User.objects.get(id = request.session['userid']))
            nt = Note.objects.filter(scholarship = scholarship_s).filter(by = by).filter(of = app)
            nt.delete()
            state = 'note deleted'
            active = 3

        ap = Applicant.objects.filter(scholarship = scholarship_s).values('applicant')
        prof = UserProfile.objects.filter(user__in = ap)
        ques = question.objects.filter(scholarship = scholarship_s)
        notes = Note.objects.filter(scholarship = scholarship_s).filter(by__id = request.session['userid'])
        app.status = state
        for  usr in prof :
            ans  = answer.objects.filter(user = usr.user).filter(question__scholarship = scholarship_s)
            usr.answ = ans
            if usr.user == app:
                usr.status = state
                usr.act = active
            try:
                usr.notes = notes.get(of = usr.user).note
            except:
                usr.notes = ''
            if Selected.objects.filter(scholarship = scholarship_s).filter(selected__id = usr.user.id).exists():
                usr.level = 'selected'
            elif ShortList.objects.filter(scholarship = scholarship_s).filter(shortlist__id = usr.user.id).exists():
                usr.level = 'shortlisted'
            elif Rejected.objects.filter(scholarship = scholarship_s).filter(rejected__id = usr.user.id).exists():
                usr.level = 'rejected'
            else:
                usr.level = 'not decided yet'
        doclist = document.objects.filter(scholarship = scholarship_s)
        for  usr in prof :
            usr.docs = UserDocuments.objects.filter(user = usr).filter(docs__in= doclist)

        context = {
            'scholarship' : scholarship_s,
            'prof' : prof,
            'url' : url,
            'pro' : User.objects.get(id = request.session['userid'])
            # 'state' : state,
        }
        return render_to_response('provider/response.html',context,RequestContext(request))
        
    return HttpResponseRedirect('/provider/response/'+url+'/')

@login_required(login_url='/provider/login/')
def shortlist(request,scholarship_name):
    url = scholarship_name
    scholarship_name = scholarship_name.replace("-","")
    i=1
    for x in scholarship.objects.all():
        s_name = re.sub('[^A-Za-z0-9]+', '', x.name)
        i=x.scholarship_id
        if s_name == scholarship_name:
            break   
    scholarship_s = scholarship.objects.filter(pk=i)
    scholarship_s = scholarship_s[0]
    app = ShortList.objects.filter(scholarship = scholarship_s).values('shortlist')
    prof = UserProfile.objects.filter(user__in = app)
    ques = question.objects.filter(scholarship = scholarship_s)
    notes = Note.objects.filter(scholarship = scholarship_s).filter(by__id = request.session['userid'])
    for  usr in prof :
        ans  = answer.objects.filter(user = usr.user).filter(question__scholarship = scholarship_s)
        usr.answ = ans
        try:
            usr.notes = notes.get(of = usr.user).note
        except:
            usr.notes = ''
        if Selected.objects.filter(scholarship = scholarship_s).filter(selected__id = usr.user.id).exists():
            usr.level = 'selected'
        elif ShortList.objects.filter(scholarship = scholarship_s).filter(shortlist__id = usr.user.id).exists():
            usr.level = 'shortlisted'
        elif Rejected.objects.filter(scholarship = scholarship_s).filter(rejected__id = usr.user.id).exists():
            usr.level = 'rejected'

    doclist = document.objects.filter(scholarship = scholarship_s)
    for  usr in prof :
        usr.docs = UserDocuments.objects.filter(user = usr).filter(docs__in= doclist)
        

    context = {
        'scholarship' : scholarship_s,
        'url' : url,
        'pro' : User.objects.get(id = request.session['userid']),
        'prof' : prof,
    }
    return render_to_response('provider/shortlist.html',context,RequestContext(request))

@login_required(login_url='/provider/login/')
def task(request):
    if request.POST:
        action = request.POST.get('action')
        app = request.POST.get('applicant')
        sch = request.POST.get('scholarship')
        url = request.POST.get('url')
        scholarship_s = scholarship.objects.get(name = sch)
        app = User.objects.get(email = app)
        #############################################################
        if action == 'task' :            
            body = request.POST.get('mess')
            import sendgrid
            sg_username = "scholfin"
            sg_password = "sameer1234"

            sg = sendgrid.SendGridClient(sg_username, sg_password)
            message = sendgrid.Mail()
            subject = request.POST.get('sub')
            message.set_from((User.objects.get(id = request.session['userid'])).email)
            message.set_subject(subject)
            message.set_text("This is text body")
            messag = body
            message.set_html(messag)
            shr = ShortList.objects.filter(scholarship = scholarship_s)[0]
            print shr.shortlist.all()
            for users in shr.shortlist.all():
                message.add_to(users.email)
            message.add_to('thescholfin@gmail.com')
            state = 'task has been mailed to all'
            status, msg = sg.send(message)
        ##############################################################
        elif action == 'select' :            
            try:
                shr = Selected.objects.get(scholarship =  scholarship_s)
                shr.selected.add(app)
                shr.count = shr.count+1
                shr.save()
            except Selected.DoesNotExist:
                shr = Selected()
                shr.scholarship = scholarship_s
                shr.save()
                shr.selected.add(app)
                shr.count = 1
                shr.save()

            try:
                shr = Rejected.objects.get(scholarship =  scholarship_s)
                try:
                    shr.rejected.remove(app)
                    shr.count = shr.count - 1
                    shr.save()
                except:
                    pass
            except:
                pass

            import sendgrid
            sg_username = "scholfin"
            sg_password = "sameer1234"

            sg = sendgrid.SendGridClient(sg_username, sg_password)
            message = sendgrid.Mail()
            subject = request.POST.get('sub')
            message.set_from("thescholfin@gmail.com")
            message.set_subject('Congrats You ave been Selected')
            message.set_text("This is text body")
            body = 'hi ' + app.first_name + ', You have been Selected for' + sch + ' For further enquiry contact the and documents details scholarship provider'
            messag = body
            message.set_html(messag)
            message.add_to(app.email)
            print app.email
            message.add_to('thescholfin@gmail.com')
            status, msg = sg.send(message)

            state = app.first_name + ' has been selected'
            active = 1

        ####################################################################
        elif action == 'reject':
            state = app.first_name + ' has been rejected'
            active = 1
            try:
                rej = Rejected.objects.get(scholarship =  scholarship_s)
                rej.rejected.add(app)
                rej.count = rej.count+1
                rej.save()
            except Rejected.DoesNotExist:
                rej = Rejected()
                rej.scholarship = scholarship_s
                rej.save()
                rej.rejected.add(app)
                rej.count = 1
                rej.save()
            try:
                shr = ShortList.objects.get(scholarship =  scholarship_s)
                try:
                    print 'ihi'
                    shr.shortlist.remove(app)
                    shr.count = shr.count - 1
                    shr.save()
                except:
                    pass
            except:
                pass
            try:
                shr = Selected.objects.get(scholarship =  scholarship_s)
                try:
                    shr.selected.remove(app)
                    shr.count = shr.count - 1
                    shr.save()
                except:
                    pass
            except:
                pass
        ####################################################################
        elif action == 'mail':
            body = request.POST.get('mess')
            import sendgrid
            sg_username = "scholfin"
            sg_password = "sameer1234"

            sg = sendgrid.SendGridClient(sg_username, sg_password)
            message = sendgrid.Mail()
            subject = request.POST.get('sub')
            message.set_from((User.objects.get(id = request.session['userid'])).email)
            message.set_subject(subject)
            message.set_text("This is text body")
            messag = body
            message.set_html(messag)
            message.add_to(app.email)
            message.add_to('thescholfin@gmail.com')
            status, msg = sg.send(message)

            state = 'email has been sent'
            active = 2
        ####################################################################
        elif action == 'savenote':
            notes = request.POST.get('notes')
            by = (User.objects.get(id = request.session['userid']))
            nt = Note.objects.filter(scholarship = scholarship_s).filter(by = by).filter(of = app)
            if len(nt) == 0 :
                new_note = Note()
                new_note.scholarship = scholarship_s
                new_note.by = by
                new_note.of = app
                new_note.note = notes
                new_note.save()
            else:
                nt = nt[0]
                nt.note = notes
                nt.save()
            state = ' note saved'
            active = 3
        ####################################################################
        elif action == 'deletenote':
            by = (User.objects.get(id = request.session['userid']))
            nt = Note.objects.filter(scholarship = scholarship_s).filter(by = by).filter(of = app)
            nt.delete()
            state = 'note deleted'
            active = 3

        ap = ShortList.objects.filter(scholarship = scholarship_s).values('shortlist')
        prof = UserProfile.objects.filter(user__in = ap)
        ques = question.objects.filter(scholarship = scholarship_s)
        notes = Note.objects.filter(scholarship = scholarship_s).filter(by__id = request.session['userid'])
        app.status = state
        for  usr in prof :
            ans  = answer.objects.filter(user = usr.user).filter(question__scholarship = scholarship_s)
            usr.answ = ans
            if usr.user == app:
                usr.status = state
                usr.act = active
            try:
                usr.notes = notes.get(of = usr.user).note
            except:
                usr.notes = ''
            if Selected.objects.filter(scholarship = scholarship_s).filter(selected__id = usr.user.id).exists():
                usr.level = 'selected'
            elif ShortList.objects.filter(scholarship = scholarship_s).filter(shortlist__id = usr.user.id).exists():
                usr.level = 'shortlisted'
            elif Rejected.objects.filter(scholarship = scholarship_s).filter(rejected__id = usr.user.id).exists():
                usr.level = 'rejected'
        doclist = document.objects.filter(scholarship = scholarship_s)
        for  usr in prof :
            usr.docs = UserDocuments.objects.filter(user = usr).filter(docs__in= doclist)
            
        context = {
            'scholarship' : scholarship_s,
            'url' : url,
            'prof' : prof,
            'pro' : User.objects.get(id = request.session['userid'])
        }
        return render_to_response('provider/shortlist.html',context,RequestContext(request))

    return HttpResponseRedirect('/provider/shortlist/'+url+'/')


@login_required(login_url='/provider/login/')
def select(request,scholarship_name):
    url = scholarship_name
    scholarship_name = scholarship_name.replace("-","")
    i=1
    for x in scholarship.objects.all():
        s_name = re.sub('[^A-Za-z0-9]+', '', x.name)
        i=x.scholarship_id
        if s_name == scholarship_name:
            break   
    scholarship_s = scholarship.objects.filter(pk=i)
    scholarship_s = scholarship_s[0]
    app = Selected.objects.filter(scholarship = scholarship_s).values('selected')
    prof = UserProfile.objects.filter(user__in = app)
    ques = question.objects.filter(scholarship = scholarship_s)
    notes = Note.objects.filter(scholarship = scholarship_s).filter(by__id = request.session['userid'])
    for  usr in prof :
        ans  = answer.objects.filter(user = usr.user).filter(question__scholarship = scholarship_s)
        usr.answ = ans
        try:
            usr.notes = notes.get(of = usr.user).note
        except:
            usr.notes = ''
    for  usr in prof :
            usr.docs = UserDocuments.objects.filter(user = usr).filter(docs__in= doclist)

    context = {
        'scholarship' : scholarship_s,
        'url' : url,
        'prof' : prof,
        'pro' : User.objects.get(id = request.session['userid']),
    }
    return render_to_response('provider/select.html',context,RequestContext(request))

@login_required(login_url='/provider/login/')
def selected(request):
    if request.POST:
        action = request.POST.get('action')
        app = request.POST.get('applicant')
        sch = request.POST.get('scholarship')
        url = request.POST.get('url')
        scholarship_s = scholarship.objects.get(name = sch)
        app = User.objects.get(email = app)
        #############################################################
        if action == 'mail' :
            body = request.POST.get('mess')
            import sendgrid
            sg_username = "scholfin"
            sg_password = "sameer1234"

            sg = sendgrid.SendGridClient(sg_username, sg_password)
            message = sendgrid.Mail()
            subject = request.POST.get('sub')
            message.set_from((User.objects.get(id = request.session['userid'])).email)
            message.set_subject(subject)
            message.set_text("This is text body")
            messag = body
            message.set_html(messag)
            message.add_to(app.email)
            message.add_to('thescholfin@gmail.com')
            status, msg = sg.send(message)

            state = 'email has been sent'
            active = 2
        ####################################################################
        elif action == 'savenote':
            notes = request.POST.get('notes')
            by = (User.objects.get(id = request.session['userid']))
            nt = Note.objects.filter(scholarship = scholarship_s).filter(by = by).filter(of = app)
            if len(nt) == 0 :
                new_note = Note()
                new_note.scholarship = scholarship_s
                new_note.by = by
                new_note.of = app
                new_note.note = notes
                new_note.save()
            else:
                nt = nt[0]
                nt.note = notes
                nt.save()
            state = ' note saved'
            active = 3
        ####################################################################
        elif action == 'deletenote':
            by = (User.objects.get(id = request.session['userid']))
            nt = Note.objects.filter(scholarship = scholarship_s).filter(by = by).filter(of = app)
            nt.delete()
            state = 'note deleted'
            active = 3
        #############################################################
        elif action == 'end' :            
            body = request.POST.get('mess')
            import sendgrid
            sg_username = "scholfin"
            sg_password = "sameer1234"

            sg = sendgrid.SendGridClient(sg_username, sg_password)
            message = sendgrid.Mail()
            subject = request.POST.get('sub')
            message.set_from((User.objects.get(id = request.session['userid'])).email)
            message.set_subject(subject)
            message.set_text("This is text body")
            messag = body
            message.set_html(messag)
            shr = Selected.objects.filter(scholarship = scholarship_s)[0]
            print shr.selected.all()
            for users in shr.selected.all():
                message.add_to(users.email)
            message.add_to('thescholfin@gmail.com')
            stats, msg = sg.send(message)
            state = 'task has been mailed to all'

        ap = Selected.objects.filter(scholarship = scholarship_s).values('selected')
        prof = UserProfile.objects.filter(user__in = ap)
        ques = question.objects.filter(scholarship = scholarship_s)
        notes = Note.objects.filter(scholarship = scholarship_s).filter(by__id = request.session['userid'])
        for  usr in prof :
            ans  = answer.objects.filter(user = usr.user).filter(question__scholarship = scholarship_s)
            usr.answ = ans
            if usr.user == app:
                usr.status = state
                usr.act = active
            try:
                usr.notes = notes.get(of = usr.user).note
            except:
                usr.notes = ''

        for  usr in prof :
            usr.docs = UserDocuments.objects.filter(user = usr).filter(docs__in= doclist)
            
        context = {
            'scholarship' : scholarship_s,
            'url' : url,
            'prof' : prof,
            'pro' : User.objects.get(id = request.session['userid']),
        }
        return render_to_response('provider/select.html',context,RequestContext(request))

    return HttpResponseRedirect('/provider/selected/'+url+'/')

@login_required(login_url='/provider/login/')
def reject(request,scholarship_name):
    url = scholarship_name
    scholarship_name = scholarship_name.replace("-","")
    i=1
    for x in scholarship.objects.all():
        s_name = re.sub('[^A-Za-z0-9]+', '', x.name)
        i=x.scholarship_id
        if s_name == scholarship_name:
            break   
    scholarship_s = scholarship.objects.filter(pk=i)
    scholarship_s = scholarship_s[0]
    app = Rejected.objects.filter(scholarship = scholarship_s).values('rejected')
    prof = UserProfile.objects.filter(user__in = app)
    context = {
        'scholarship' : scholarship_s,
        'url' : url,
        'prof' : prof,
        'pro' : User.objects.get(id = request.session['userid'])
    }
    return render_to_response('provider/reject.html',context,RequestContext(request))


@login_required(login_url='/provider/login/')
def unreject(request):
    if request.POST:
        app = request.POST.get('applicant')
        sch = request.POST.get('scholarship')
        url = request.POST.get('url')
        scholarship_s = scholarship.objects.get(name = sch)
        app = User.objects.get(email = app)
        shr = Rejected.objects.get(scholarship =  scholarship_s)
        shr.rejected.remove(app)
        shr.count = shr.count - 1
        shr.save()
        app = Rejected.objects.filter(scholarship = scholarship_s).values('rejected')
        prof = UserProfile.objects.filter(user__in = app)
        context = {
            'scholarship' : scholarship_s,
            'url' : url,
            'prof' : prof,
            'pro' : User.objects.get(id = request.session['userid'])
        }
        return render_to_response('provider/reject.html',context,RequestContext(request))

def genfiles(request):
    if request.is_ajax():
        scholarship_name = request.GET.get('val')      
        scholarship_name = scholarship_name.replace("-","")
        i=1
        for x in scholarship.objects.all():
            s_name = re.sub('[^A-Za-z0-9]+', '', x.name)
            i=x.scholarship_id
            if s_name == scholarship_name:
                break   
        scholarship_s = scholarship.objects.filter(pk=i)
        scholarship_s = scholarship_s[0]
        typee = str(request.GET.get('type'))
        if typee == 'applicant':
            app = Applicant.objects.filter(scholarship__name = scholarship_s).values('applicant')
        elif typee == 'shortlist':
            app = ShortList.objects.filter(scholarship__name = scholarship_s).values('shortlist')
        elif typee== 'select' :
            app = Selected.objects.filter(scholarship__name = scholarship_s).values('selected')


        prof = UserProfile.objects.filter(user__in = app)
        ques = question.objects.filter(scholarship = scholarship_s)
        listt = []
        for appl in prof:
            dictt = {}
            for x in ques : 
                ans = answer.objects.filter(user = appl.user).filter(question=x)[0]
                ans = str(ans.answer)
                dictt[str(x.question.strip())] = ans.strip()
            if appl.user_disability == 0:
                dis =  'NO'
            else :
                dis = 'YES'
            if appl.user_gender == 0:
                gender =  'Male'
            else :
                gender = 'Female'
            if appl.user_income is None :
                coll = 'NA'
            else:
                coll = str(appl.user_income)


            name = str(appl.user.first_name) + ' ' + str(appl.user.last_name)
            caste = str(appl.user_caste)
            religion = str(appl.user_religion)
            field = str(appl.user_field)
            level  = str(appl.user_level)
            state = str(appl.user_state)
            email = str(appl.user.email)
            dictt['Gender'] = gender
            dictt['Disability'] = dis
            dictt["Education caste"] = caste
            dictt["religion"] = religion
            dictt["Education field"] = field
            dictt["Education level"] = level
            dictt["Education state"] = state
            dictt["College"] = coll
            dictt["Email"] = email             
            dictt["Name"] =  name
            

            listt.append(dictt)
            print dictt
        import json
        return HttpResponse(json.dumps(listt))

    elif request.POST :
        import reportlab
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.translate(inch,inch)
        # define a large font
        p.setFont("Helvetica", 14)
        # choose some colors
        p.setStrokeColorRGB(0.2,0.5,0.3)
        p.setFillColorRGB(1,0,1)
        # draw some lines
        p.line(0,0,0,1.7*inch)
        p.line(0,0,1*inch,0)
        # draw a rectangle
        p.rect(0.2*inch,0.2*inch,1*inch,1.5*inch, fill=1)
        # make text go straight up
        p.rotate(90)
        # change color
        p.setFillColorRGB(0,0,0.77)
        # say hello (note after rotate the y coord needs to be negative!)
        p.drawString(0.3*inch, -inch, "Hello World")


        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response
        # import csv
        # response = HttpResponse(content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename="somefilename.xlsx"'

        # writer = csv.writer(response)
        # writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
        # writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

        # return response

def form(request):
    if request.POST:
        if request.POST.get('upload') == 'upload' :
            user = User.objects.get(id = request.session['userid'])
            scholarships = scholarship.objects.get(name = 'J.N. Tata Endowment for Higher Education')
            questions = question.objects.filter(scholarship = scholarships)
            email = user.email
            import csv
            with open('static/download_tata.csv','rb') as csvfile:
                spamreader = csv.reader(csvfile, quotechar='|')
                for row in spamreader:
                    if any(email in s for s in row):
                        i=1
                        print 'gotthe  match',len(row)
                        for ques in questions:
                            new_answer = answer()           
                            new_answer.question = ques
                            new_answer.user = user
                            new_answer.save()
                            new_answer.answer = row[i]          
                            new_answer.save()
                            i += 1
                        break
            if not UserDocuments.objects.filter(user = UserProfile.objects.get(user = user)).filter(docs__in = document.objects.filter(scholarship = scholarships)).exists():
                if len(request.FILES.getlist('file')) > 0 :
                    for i in range (1, len(document.objects.filter(scholarship = scholarships))+1):
                        doc =  UserDocuments()
                        doc.user = UserProfile.objects.get(user = user)
                        doc.docs = document.objects.filter(scholarship = scholarships)[i-1]
                        doc.files = request.FILES.getlist('file')[i-1]
                        doc.save()
            
            try:
                app = Applicant.objects.get(scholarship =  scholarships)
                app.applicant.add(user)
                app.count = app.count+1
                app.save()
            except Applicant.DoesNotExist:
                new_app = Applicant()
                new_app.scholarship = scholarships
                new_app.save()
                new_app.applicant.add(user)
                new_app.count = 1
                new_app.save()
            acti = activity.objects.filter(scholarship=scholarships).filter(user=user).filter(activity=' just applied for your Scholarship')
            if len(acti) > 0:
                acti=acti[0]
                acti.timestamp = timezone.now()
            else:
                act = activity()
                act.user = user
                act.scholarship = scholarships
                act.activity = ' just applied for your Scholarship'
                act.save()
                    
            subject = "Application for " +scholarships.name + ' is successfull'
            messag = "Hi "+user.first_name+',<br>' + 'We have received your Application for ' + scholarships.name +'.<br>' + 'For further details you can contact ' +'<br>' + scholarships.contact_details

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
            try:
                status, msg = sg.send(message)
            except : 
                print status

            message1 = sendgrid.Mail()
            provider = Provider.objects.filter(scholarship = scholarships)[0]
            subject = "New Application for " +scholarships.name + 'from ' + user.first_name 
            messag = "Hi "+provider.user.email+',<br><br>' + 'You have received new your Application for ' + scholarships.name +'.<br>' + 'For further tracking you should visit the Scholfin here www.scholfin.com/provider/ <br><br> Thanks, <br> Team Scholfin' 
            message1.set_from("thescholfin@gmail.com")
            message1.set_subject(subject)
            message1.set_text("This is text body")
            message1.set_html(messag)
            message1.add_to(provider.user.email)
            message1.add_to('thescholfin@gmail.com')
            status, msg = sg.send(message1)
            return HttpResponseRedirect('/dashboard/')

        else:
            import csv
            mylist = []
            myfile = open('static/download_tata.csv','a')
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            scholarships = scholarship.objects.get(name = 'J.N. Tata Endowment for Higher Education')
            questions = question.objects.filter(scholarship = scholarships)
            user = User.objects.get(id = request.session['userid'])
            mylist.append(user.email)
            for ques in questions:
                if ques.question_type < 3  or ques.question_type == 4:
                    ans = request.POST.get(str(ques.question_id))
                    mylist.append(ans)
                else:
                    ans = ''
                    listt = request.POST.getlist(str(ques.question_id))
                    for x in listt:
                        ans = ans + str(x)
                    mylist.append(ans)
            
            wr.writerow(mylist)
            myfile.close()
        # response = HttpResponse(content_type='application/vnd.ms-excel.sheet.macroEnabled.12')
        # response['Content-Disposition'] = 'attachment; filename="ABC.xlsm"'
            return HttpResponseRedirect('/static/Application Endownment-Form.xlsm',{'state' : 'state'})

