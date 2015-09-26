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



@login_required(login_url='/login/')
def gov(request):
    context = RequestContext(request)
    user_data = UserProfile.objects.filter(user__username=request.user.username)
    user_data= user_data[0]
    print user_data


    # user dictionary for the searching

    user_table = {
        'state':user_data.user_state,
        'level':user_data.user_level,
        'religion':user_data.user_religion,
        'caste':user_data.user_caste,
        'field':user_data.user_field,
        'abroad':user_data.user_abroad,
        'gender':user_data.user_gender,

    }


    scholarships = scholarship.objects.filter(education_state__state_name=user_table['state']).filter(
        education_level__level_name=user_table['level']).filter(education_religion__religion_name=user_table['religion']).filter(
        education_caste__caste_name=user_table['caste']).filter(education_field__field_name=user_table['field'])


    scholarship_interest=[]
    for s in scholarships:
        matched=0;
        interests=interest.objects.filter(scholarship=s)
        interests_count=interest.objects.filter(scholarship=s).count()
        user_interest=interest.objects.filter(userprofile=user_data)
        if interests_count==0:
            scholarship_interest.append(s)
        else :
            for intrst in interests:
                for intrst_u in user_interest:
                    if intrst==intrst_u:
                        matched=1
            if matched==1:
                scholarship_interest.append(s)



    scholarship_gender=[]
    if user_data.user_gender ==1:
        scholarship_gender=scholarship_interest
    else :
        for s in scholarship_interest:
            #print s.gender
            if s.gender == 0:
                scholarship_gender.append(s)


    scholarship_abroad=[]
    country = abroad.objects.filter(userprofile=user_data)
    c=country[0]
    c=str(c)

    if c==("India"):
        for s in scholarship_gender:
            country = abroad.objects.filter(scholarship=s)
            country_count = abroad.objects.filter(scholarship=s).count()
            if(country_count==1):
                if(str(country[0])== 'India'):
                    scholarship_abroad.append(s)
    else:
        scholarship_abroad = scholarship_gender



    scholarship_disability=[]
    if user_data.user_disability == 0:
        for s in scholarship_abroad:
            if s.disability !=1:
                scholarship_disability.append(s)
    else:
        scholarship_disability=scholarship_abroad

    scholarship_government=[]

    for s in scholarship_disability:
        if s.scholarship_type==1:
            scholarship_government.append(s)


    number_of_scholarships = 0
    amount = 0
    sctype1={}
    for sc in scholarship_government:
        number_of_scholarships = number_of_scholarships + 1
        amount = amount + amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
        sctype1[sc.scholarship_id]=sctype(sc.amount_frequency,sc.amount)
    amount = int(amount)
    amount = indianformat(amount)


    context_list = {
        'scholarships': scholarship_government,
        'number': number_of_scholarships,
        'amount': amount,
        'sctype1':sctype1,
        'user':user_data,

    }


    return render_to_response('scholarship/fin_dash.html', context_list, context)


@login_required(login_url='/login/')
def pri(request):
    context = RequestContext(request)
    user_data = UserProfile.objects.filter(user__username=request.user.username)
    user_data= user_data[0]
    # user dictionary for the searching

    user_table = {
        'state':user_data.user_state,
        'level':user_data.user_level,
        'religion':user_data.user_religion,
        'caste':user_data.user_caste,
        'field':user_data.user_field,
        'abroad':user_data.user_abroad,
        'gender':user_data.user_gender,

    }


    scholarships = scholarship.objects.filter(education_state__state_name=user_table['state']).filter(
        education_level__level_name=user_table['level']).filter(education_religion__religion_name=user_table['religion']).filter(
        education_caste__caste_name=user_table['caste']).filter(education_field__field_name=user_table['field'])


    scholarship_interest=[]
    for s in scholarships:
        matched=0;
        interests=interest.objects.filter(scholarship=s)
        interests_count=interest.objects.filter(scholarship=s).count()
        user_interest=interest.objects.filter(userprofile=user_data)
        if interests_count==0:
            scholarship_interest.append(s)
        else :
            for intrst in interests:
                for intrst_u in user_interest:
                    if intrst==intrst_u:
                        matched=1
            if matched==1:
                scholarship_interest.append(s)


    scholarship_gender=[]
    if user_data.user_gender ==1:
        scholarship_gender=scholarship_interest
    else :
        for s in scholarship_interest:
            #print s.gender
            if s.gender == 0:
                scholarship_gender.append(s)

    scholarship_abroad=[]
    country = abroad.objects.filter(userprofile=user_data)
    c=country[0]
    c=str(c)

    if c==("India"):
        for s in scholarship_gender:
            country = abroad.objects.filter(scholarship=s)
            country_count = abroad.objects.filter(scholarship=s).count()
            if(country_count==1):
                if(str(country[0])== 'India'):
                    scholarship_abroad.append(s)
    else:
        scholarship_abroad = scholarship_gender

    scholarship_disability=[]
    if user_data.user_disability == 0:
        for s in scholarship_abroad:
            if s.disability !=1:
                scholarship_disability.append(s)
    else:
        scholarship_disability=scholarship_abroad


    scholarship_private=[]

    for s in scholarship_disability:
        if s.scholarship_type==0:
            scholarship_private.append(s)

    number_of_scholarships = 0
    amount = 0
    sctype1={}
    for sc in scholarship_private:
        number_of_scholarships = number_of_scholarships + 1
        amount = amount + amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
        sctype1[sc.scholarship_id]=sctype(sc.amount_frequency,sc.amount)
    amount = int(amount)
    print amount
    amount = indianformat(amount)
    context_list = {
        'scholarships': scholarship_private,
        'number': number_of_scholarships,
        'amount': amount,
        'sctype1':sctype1,
        'user':user_data,

    }
    return render_to_response('scholarship/fin_dash.html', context_list, context)


@login_required(login_url='/login/')
def comp(request):
    context = RequestContext(request)
    user_data = UserProfile.objects.filter(user__username=request.user.username)
    user_data= user_data[0]
    print user_data


    # user dictionary for the searching

    user_table = {
        'state':user_data.user_state,
        'level':user_data.user_level,
        'religion':user_data.user_religion,
        'caste':user_data.user_caste,
        'field':user_data.user_field,
        'abroad':user_data.user_abroad,
        'gender':user_data.user_gender,

    }



    scholarships = scholarship.objects.filter(education_state__state_name=user_table['state']).filter(
        education_level__level_name=user_table['level']).filter(education_religion__religion_name=user_table['religion']).filter(
        education_caste__caste_name=user_table['caste']).filter(education_field__field_name=user_table['field'])


    scholarship_interest=[]


    for s in scholarships:
        matched=0;
        interests=interest.objects.filter(scholarship=s)
        interests_count=interest.objects.filter(scholarship=s).count()
        user_interest=interest.objects.filter(userprofile=user_data)
        if interests_count==0:
            scholarship_interest.append(s)
        else :
            for intrst in interests:
                for intrst_u in user_interest:
                    if intrst==intrst_u:
                        matched=1
            if matched==1:
                scholarship_interest.append(s)

	scholarship_gender=[]
    if user_data.user_gender ==1:
        scholarship_gender=scholarship_interest
    else :
        for s in scholarship_interest:
            #print s.gender
            if s.gender == 0:
                scholarship_gender.append(s)



    scholarship_abroad=[]
    country = abroad.objects.filter(userprofile=user_data)
    c=country[0]
    c=str(c)



    if c==("India"):
        for s in scholarship_gender:
            country = abroad.objects.filter(scholarship=s)
            country_count = abroad.objects.filter(scholarship=s).count()
            if(country_count==1):
                if(str(country[0])== 'India'):
                    scholarship_abroad.append(s)
    else:
        scholarship_abroad = scholarship_gender



    scholarship_disability=[]
    if user_data.user_disability == 0:
        for s in scholarship_abroad:
            if s.disability !=1:
                scholarship_disability.append(s)
    else:
        scholarship_disability=scholarship_abroad
   
    scholarship_competitions=[]

    for s in scholarship_disability:
        if s.scholarship_type==2:
            scholarship_competitions.append(s)

    number_of_scholarships = 0
    amount = 0
    sctype1={}
    for sc in scholarship_competitions:
        number_of_scholarships = number_of_scholarships + 1
        amount = amount + amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
        sctype1[sc.scholarship_id]=sctype(sc.amount_frequency,sc.amount)
    amount = int(amount)
    print amount
    amount = indianformat(amount)
    context_list = {
        'scholarships': scholarship_competitions,
        'number': number_of_scholarships,
        'amount': amount,
        'sctype1':sctype1,
        'user':user_data,

    }


    return render_to_response('scholarship/fin_dash.html', context_list, context)
