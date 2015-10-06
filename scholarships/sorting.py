__author__ = 'nishant'

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from functions import *
from scholarships.models import *
from scholarships.models import *
import re

def discard_passed(scholarships):
    from django.utils import timezone

    after_discarded = []
    year_long = []
    not_declared = []
    current = timezone.now()

    for schlrshp in scholarships:
        if schlrshp.deadline_type == 0 or schlrshp.deadline_type == 3:
            if schlrshp.deadline > current:
                after_discarded.append(schlrshp)

        elif schlrshp.deadline_type == 1:
            year_long.append(schlrshp)

        else:
            not_declared.append(schlrshp)

    after_discarded.extend(year_long)
    after_discarded.extend(not_declared)
    return after_discarded


@login_required(login_url='/login/')
def state_only(request , scholarship_state):
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
    print len(scholarship_interest)
    scholarship_gender=[]
    if user_data.user_gender ==1:
        scholarship_gender=scholarship_interest
    else :
        for s in scholarship_interest:
            #print s.gender
            if s.gender == 0:
                scholarship_gender.append(s)
    print len(scholarship_gender)

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


    # declaring a empty array for storing the results
    scholarship_state_only = []

    for s in scholarship_disability:
        state_count = state.objects.filter(scholarship=s).count()
        print state_count
        if state_count==1:
            scholarship_state_only.append(s)

    number_of_scholarships = 0
    amount = 0
    sctype1={}
    for sc in scholarship_state_only:
        number_of_scholarships = number_of_scholarships + 1
        amount = amount + amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
        sctype1[sc.scholarship_id]=sctype(sc.amount_frequency,sc.amount)
        x = re.sub('[^A-Za-z0-9]+',' ',sc.name)
        x = x.strip(' ')
        x = re.sub('[^A-Za-z0-9]+','-',x)
        sc.url = x;
    amount = int(amount)
    print amount
    amount = indianformat(amount)

    scholarship_state_only = discard_passed(scholarship_state_only)
    
    #####Sorting list on basis of deadline and amount
    sort_by = request.GET.get('sort_by',False)
    if sort_by:
        if sort_by == 'deadline_a' or sort_by == 'deadline_d':
            for_sorting = [] #deadline_type= 0&3
            year_long = [] #deadline_type= 1
            not_declared = [] #deadline_type= 2

            for schlrshp in scholarship_state_only:
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
            for sc in scholarship_state_only:
                amount = amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
                for_sorting.append((sc, amount))

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
            'scholarships': scholarship_state_only,
            'number': number_of_scholarships,
            'amount': amount,
            'sctype1':sctype1,
            'user':user_data,
            'sorted_by': '',
            }

    else:
        context_list = {
        'scholarships': scholarship_state_only,
        'number': number_of_scholarships,
        'amount': amount,
        'sctype1':sctype1,
        'user':user_data,
        'sorted_by': '',
        }

    return render_to_response('scholarship/fin_dash.html', context_list, context)



@login_required(login_url='/login/')
def interest_only(request):
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
        for intrst in interests:
            for intrst_u in user_interest:
                if intrst==intrst_u:
                    matched=1
        if matched==1:
            scholarship_interest.append(s)
    print len(scholarship_interest)
    scholarship_gender=[]
    if user_data.user_gender ==1:
        scholarship_gender=scholarship_interest
    else :
        for s in scholarship_interest:
            #print s.gender
            if s.gender == 0:
                scholarship_gender.append(s)
    print len(scholarship_gender)

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

    number_of_scholarships = 0
    amount = 0
    sctype1={}
    for sc in scholarship_disability:
        number_of_scholarships = number_of_scholarships + 1
        amount = amount + amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
        sctype1[sc.scholarship_id]=sctype(sc.amount_frequency,sc.amount)
        x = re.sub('[^A-Za-z0-9]+',' ',sc.name)
        x = x.strip(' ')
        x = re.sub('[^A-Za-z0-9]+','-',x)
        sc.url = x;
    amount = int(amount)
    print amount
    amount = indianformat(amount)

    scholarship_disability = discard_passed(scholarship_disability)

    #####Sorting list on basis of deadline and amount
    sort_by = request.GET.get('sort_by',False)
    if sort_by:
        if sort_by == 'deadline_a' or sort_by == 'deadline_d':
            for_sorting = [] #deadline_type= 0&3
            year_long = [] #deadline_type= 1
            not_declared = [] #deadline_type= 2

            for schlrshp in scholarship_disability:
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
            for sc in scholarship_disability:
                amount = amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
                for_sorting.append((sc, amount))

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
            'scholarships': scholarship_disability,
            'number': number_of_scholarships,
            'amount': amount,
            'sctype1':sctype1,
            'user':user_data,
            'sorted_by': '',
            }

    else:
        context_list = {
        'scholarships': scholarship_disability,
        'number': number_of_scholarships,
        'amount': amount,
        'sctype1':sctype1,
        'user':user_data,
        'sorted_by': '',
        }

    return render_to_response('scholarship/fin_dash.html', context_list, context)


@login_required(login_url='/login/')
def india_only(request):
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
    print len(scholarship_interest)
    scholarship_gender=[]

    if user_data.user_gender ==1:
        scholarship_gender=scholarship_interest
    else :
        for s in scholarship_interest:
            #print s.gender
            if s.gender == 0:
                scholarship_gender.append(s)

    scholarship_india=[]

    for s in scholarship_gender:
        country = abroad.objects.filter(scholarship=s)[0]
        countries_count = abroad.objects.filter(scholarship=s).count()
        if countries_count==1 and str(country) == 'India':
            scholarship_india.append(s)


    scholarship_disability=[]
    if user_data.user_disability == 0:
        for s in scholarship_india:
            if s.disability !=1:
                scholarship_disability.append(s)
    else:
        scholarship_disability=scholarship_abroad

    number_of_scholarships = 0
    amount = 0
    sctype1={}
    for sc in scholarship_disability:
        number_of_scholarships = number_of_scholarships + 1
        amount = amount + amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
        sctype1[sc.scholarship_id]=sctype(sc.amount_frequency,sc.amount)
        x = re.sub('[^A-Za-z0-9]+',' ',sc.name)
        x = x.strip(' ')
        x = re.sub('[^A-Za-z0-9]+','-',x)
        sc.url = x;
    amount = int(amount)
    print amount
    amount = indianformat(amount)

    scholarship_disability = discard_passed(scholarship_disability)

    #####Sorting list on basis of deadline and amount
    sort_by = request.GET.get('sort_by',False)
    if sort_by:
        if sort_by == 'deadline_a' or sort_by == 'deadline_d':
            for_sorting = [] #deadline_type= 0&3
            year_long = [] #deadline_type= 1
            not_declared = [] #deadline_type= 2

            for schlrshp in scholarship_disability:
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
            for sc in scholarship_disability:
                amount = amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
                for_sorting.append((sc, amount))

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
            'scholarships': scholarship_disability,
            'number': number_of_scholarships,
            'amount': amount,
            'sctype1':sctype1,
            'user':user_data,
            'sorted_by': '',
            }

    else:
        context_list = {
        'scholarships': scholarship_disability,
        'number': number_of_scholarships,
        'amount': amount,
        'sctype1':sctype1,
        'user':user_data,
        'sorted_by': '',
        }

    return render_to_response('scholarship/fin_dash.html', context_list, context)




@login_required(login_url='/login/')
def abroad_only(request):
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
    scholarships_count = scholarship.objects.filter(education_state__state_name=user_table['state']).filter(
        education_level__level_name=user_table['level']).filter(education_religion__religion_name=user_table['religion']).filter(
        education_caste__caste_name=user_table['caste']).filter(education_field__field_name=user_table['field']).count()
    print scholarships_count
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
    print "length of interest id "+str(len(scholarship_interest))
    if user_data.user_gender ==1:
        scholarship_gender=scholarship_interest
    else :
        for s in scholarship_interest:
            #print s.gender
            if s.gender == 0:
                scholarship_gender.append(s)
    print "length of gender id "+str(len(scholarship_gender))
    scholarship_abroad=[]
    for s in scholarship_gender:
        country = abroad.objects.filter(scholarship=s)[0]
        countries_count = abroad.objects.filter(scholarship=s).count()
        if countries_count==1 and str(country) == 'India':
            '''do nothing'''
        else:
            scholarship_abroad.append(s)

    scholarship_disability=[]
    if user_data.user_disability == 0:
        for s in scholarship_abroad:
            if s.disability !=1:
                scholarship_disability.append(s)
    else:
        scholarship_disability=scholarship_abroad

    number_of_scholarships = 0
    amount = 0
    sctype1={}
    for sc in scholarship_disability:
        number_of_scholarships = number_of_scholarships + 1
        amount = amount + amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
        sctype1[sc.scholarship_id]=sctype(sc.amount_frequency,sc.amount)
        x = re.sub('[^A-Za-z0-9]+',' ',sc.name)
        x = x.strip(' ')
        x = re.sub('[^A-Za-z0-9]+','-',x)
        sc.url = x;
    amount = int(amount)
    amount = indianformat(amount)

    scholarship_disability = discard_passed(scholarship_disability)

    #####Sorting list on basis of deadline and amount
    sort_by = request.GET.get('sort_by',False)
    if sort_by:
        if sort_by == 'deadline_a' or sort_by == 'deadline_d':
            for_sorting = [] #deadline_type= 0&3
            year_long = [] #deadline_type= 1
            not_declared = [] #deadline_type= 2

            for schlrshp in scholarship_disability:
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
            for sc in scholarship_disability:
                amount = amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
                for_sorting.append((sc, amount))

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
            'scholarships': scholarship_disability,
            'number': number_of_scholarships,
            'amount': amount,
            'sctype1':sctype1,
            'user':user_data,
            'sorted_by': '',
            }

    else:
        context_list = {
        'scholarships': scholarship_disability,
        'number': number_of_scholarships,
        'amount': amount,
        'sctype1':sctype1,
        'user':user_data,
        'sorted_by': '',
        }

    return render_to_response('scholarship/fin_dash.html', context_list, context)


@login_required(login_url='/login/')
def caste_only(request):
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
    print len(scholarship_interest)
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
    print len(scholarship_abroad)

    scholarship_caste_only = []

    for s in scholarship_disability:
        caste_count = caste.objects.filter(scholarship=s).count()
        if caste_count==1:
            scholarship_caste_only.append(s)

    number_of_scholarships = 0
    amount = 0
    sctype1={}
    for sc in scholarship_caste_only:
        number_of_scholarships = number_of_scholarships + 1
        amount = amount + amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
        sctype1[sc.scholarship_id]=sctype(sc.amount_frequency,sc.amount)
        x = re.sub('[^A-Za-z0-9]+',' ',sc.name)
        x = x.strip(' ')
        x = re.sub('[^A-Za-z0-9]+','-',x)
        sc.url = x;
    amount = int(amount)
    print amount
    amount = indianformat(amount)

    scholarship_caste_only = discard_passed(scholarship_caste_only)

    #####Sorting list on basis of deadline and amount
    sort_by = request.GET.get('sort_by',False)
    if sort_by:
        if sort_by == 'deadline_a' or sort_by == 'deadline_d':
            for_sorting = [] #deadline_type= 0&3
            year_long = [] #deadline_type= 1
            not_declared = [] #deadline_type= 2

            for schlrshp in scholarship_caste_only:
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
            for sc in scholarship_caste_only:
                amount = amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
                for_sorting.append((sc, amount))

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
            'scholarships': scholarship_caste_only,
            'number': number_of_scholarships,
            'amount': amount,
            'sctype1':sctype1,
            'user':user_data,
            'sorted_by': '',
            }

    else:
        context_list = {
        'scholarships': scholarship_caste_only,
        'number': number_of_scholarships,
        'amount': amount,
        'sctype1':sctype1,
        'user':user_data,
        'sorted_by': '',
        }

    return render_to_response('scholarship/fin_dash.html', context_list, context)



@login_required(login_url='/login/')
def religion_only(request):
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
    print len(scholarship_interest)
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
    print len(scholarship_abroad)

    scholarship_religion_only = []

    for s in scholarship_disability:
        religion_count = religion.objects.filter(scholarship=s).count()
        if religion_count==1:
            scholarship_religion_only.append(s)

    number_of_scholarships = 0
    amount = 0
    sctype1={}
    for sc in scholarship_religion_only:
        number_of_scholarships = number_of_scholarships + 1
        amount = amount + amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
        sctype1[sc.scholarship_id]=sctype(sc.amount_frequency,sc.amount)
        x = re.sub('[^A-Za-z0-9]+',' ',sc.name)
        x = x.strip(' ')
        x = re.sub('[^A-Za-z0-9]+','-',x)
        sc.url = x
    amount = int(amount)
    print amount
    amount = indianformat(amount)

    scholarship_religion_only = discard_passed(scholarship_religion_only)

    #####Sorting list on basis of deadline and amount
    sort_by = request.GET.get('sort_by',False)
    if sort_by:
        if sort_by == 'deadline_a' or sort_by == 'deadline_d':
            for_sorting = [] #deadline_type= 0&3
            year_long = [] #deadline_type= 1
            not_declared = [] #deadline_type= 2

            for schlrshp in scholarship_religion_only:
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
            for sc in scholarship_religion_only:
                amount = amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
                for_sorting.append((sc, amount))

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
            'scholarships': scholarship_religion_only,
            'number': number_of_scholarships,
            'amount': amount,
            'sctype1':sctype1,
            'user':user_data,
            'sorted_by': '',
            }

    else:
        context_list = {
        'scholarships': scholarship_religion_only,
        'number': number_of_scholarships,
        'amount': amount,
        'sctype1':sctype1,
        'user':user_data,
        'sorted_by': '',
        }

    return render_to_response('scholarship/fin_dash.html', context_list, context)