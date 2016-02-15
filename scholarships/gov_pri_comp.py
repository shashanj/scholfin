from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from .sorting import *
from django.contrib.auth.models import User
import re
from .functions import *
from scholarships.models import *



@login_required(login_url='/login/')
def gov(request):
    context = RequestContext(request)
    user_data = UserProfile.objects.filter(user__username=request.user.username)
    user_data= user_data[0]
    #print user_data


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
    ss=[]
    scholarshipss = scholarship.objects.filter(education_state__state_name=user_table['state']).filter(
        education_level__level_name=user_table['level']).filter(education_religion__religion_name=user_table['religion']).filter(
        education_caste__caste_name=user_table['caste']).filter(education_field__field_name=user_table['field'])
    
    for schlrshp in scholarshipss:
        if schlrshp.deadline_type == 1:
            ss.append(schlrshp)
        elif schlrshp.deadline_type == 2:
            ss.append(schlrshp)

    scholarships = scholarship.objects.all().filter(deadline__gte=datetime.now()).filter(education_state__state_name=user_table['state']).filter(
        education_level__level_name=user_table['level']).filter(education_religion__religion_name=user_table['religion']).filter(
        education_caste__caste_name=user_table['caste']).filter(education_field__field_name=user_table['field']).filter(deadline_type = 0)


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

    for s in ss:
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
            ##print s.gender
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

    scholarship_d=[]

    for s in scholarship_disability:
        if s.scholarship_type==1:
            scholarship_d.append(s)


    number_of_scholarships = 0
    amount = 0
    sctype1={}
    for sc in scholarship_d:
        number_of_scholarships = number_of_scholarships + 1
        amount = amount + amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
        sctype1[sc.scholarship_id]=sctype(sc.amount_frequency,sc.amount)
        x = re.sub('[^A-Za-z0-9]+',' ',sc.name)
        x = x.strip(' ')
        x = re.sub('[^A-Za-z0-9]+','-',x)
        sc.url = x;
    amount = int(amount)
    amount = indianformat(amount)

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
                'user':user_data,
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
                'user':user_data,
                'sorted_by':'Deadline(Descending order)',
                }

        elif sort_by == 'amount_a' or sort_by == 'amount_d':
            for_sorting = []
            final_sorted = []
            for sc in scholarship_d:
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
            'user':user_data,
            'sorted_by': sorted_by,
            }


        else:
            context_list = {
                'scholarships': scholarship_d,
                'number': number_of_scholarships,
                'amount': amount,
                'sctype1':sctype1,
                'user':user_data,
                'sorted_by': '',

            }
    else:
        context_list = {
            'scholarships': scholarship_d,
            'number': number_of_scholarships,
            'amount': amount,
            'sctype1':sctype1,
            'user':user_data,
            'sorted_by': '',

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
    ss=[]
    scholarshipss = scholarship.objects.filter(education_state__state_name=user_table['state']).filter(
        education_level__level_name=user_table['level']).filter(education_religion__religion_name=user_table['religion']).filter(
        education_caste__caste_name=user_table['caste']).filter(education_field__field_name=user_table['field'])
    
    for schlrshp in scholarshipss:
        if schlrshp.deadline_type == 1:
            ss.append(schlrshp)
        elif schlrshp.deadline_type == 2:
            ss.append(schlrshp)

    scholarships = scholarship.objects.all().filter(deadline__gte=datetime.now()).filter(education_state__state_name=user_table['state']).filter(
        education_level__level_name=user_table['level']).filter(education_religion__religion_name=user_table['religion']).filter(
        education_caste__caste_name=user_table['caste']).filter(education_field__field_name=user_table['field']).filter(deadline_type = 0)


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

    for s in ss:
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
            ##print s.gender
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
        x = re.sub('[^A-Za-z0-9]+',' ',sc.name)
        x = x.strip(' ')
        x = re.sub('[^A-Za-z0-9]+','-',x)
        sc.url = x;
    amount = int(amount)
    print("hii")
    print(scholarship_private)
    amount = indianformat(amount)

    #####Sorting list on basis of deadline and amount
    sort_by = request.GET.get('sort_by',False)
    if sort_by:
        if sort_by == 'deadline_a' or sort_by == 'deadline_d':
            for_sorting = [] #deadline_type= 0&3
            year_long = [] #deadline_type= 1
            not_declared = [] #deadline_type= 2

            for schlrshp in scholarship_private:
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
                'user':user_data,
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
                'user':user_data,
                'sorted_by':'Deadline(Descending order)',
                }

        elif sort_by == 'amount_a' or sort_by == 'amount_d':
            for_sorting = []
            final_sorted = []
            for sc in scholarship_private:
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
            'user':user_data,
            'sorted_by': sorted_by,
            }


        else:
            context_list = {
                'scholarships': scholarship_private,
                'number': number_of_scholarships,
                'amount': amount,
                'sctype1':sctype1,
                'user':user_data,
                'sorted_by': '',

            }
    else:
        context_list = {
            'scholarships': scholarship_private,
            'number': number_of_scholarships,
            'amount': amount,
            'sctype1':sctype1,
            'user':user_data,
            'sorted_by': '',
        }
    return render_to_response('scholarship/fin_dash.html', context_list, context)


@login_required(login_url='/login/')
def comp(request):
    context = RequestContext(request)
    user_data = UserProfile.objects.filter(user__username=request.user.username)
    user_data= user_data[0]
    #print user_data


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

    ss=[]
    scholarshipss = scholarship.objects.filter(education_state__state_name=user_table['state']).filter(
        education_level__level_name=user_table['level']).filter(education_religion__religion_name=user_table['religion']).filter(
        education_caste__caste_name=user_table['caste']).filter(education_field__field_name=user_table['field'])
    
    for schlrshp in scholarshipss:
        if schlrshp.deadline_type == 1:
            ss.append(schlrshp)
        elif schlrshp.deadline_type == 2:
            ss.append(schlrshp)

    scholarships = scholarship.objects.all().filter(deadline__gte=datetime.now()).filter(education_state__state_name=user_table['state']).filter(
        education_level__level_name=user_table['level']).filter(education_religion__religion_name=user_table['religion']).filter(
        education_caste__caste_name=user_table['caste']).filter(education_field__field_name=user_table['field']).filter(deadline_type = 0)


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

    for s in ss:
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
            ##print s.gender
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
   
    scholarship_d=[]

    for s in scholarship_disability:
        if s.scholarship_type==2:
            scholarship_d.append(s)

    number_of_scholarships = 0
    amount = 0
    sctype1={}
    for sc in scholarship_d:
        number_of_scholarships = number_of_scholarships + 1
        amount = amount + amount_tot(sc.currency, sc.amount, sc.amount_frequency, sc.amount_period)
        sctype1[sc.scholarship_id]=sctype(sc.amount_frequency,sc.amount)
        x = re.sub('[^A-Za-z0-9]+',' ',sc.name)
        x = x.strip(' ')
        x = re.sub('[^A-Za-z0-9]+','-',x)
        sc.url = x;
    amount = int(amount)
    #print amount
    amount = indianformat(amount)
    
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
                'user':user_data,
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
                'user':user_data,
                'sorted_by':'Deadline(Descending order)',
                }

        elif sort_by == 'amount_a' or sort_by == 'amount_d':
            for_sorting = []
            final_sorted = []
            for sc in scholarship_d:
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
            'user':user_data,
            'sorted_by': sorted_by,
            }


        else:
            context_list = {
                'scholarships': scholarship_d,
                'number': number_of_scholarships,
                'amount': amount,
                'sctype1':sctype1,
                'user':user_data,
                'sorted_by': '',

            }
    else:
        context_list = {
            'scholarships': scholarship_d,
            'number': number_of_scholarships,
            'amount': amount,
            'sctype1':sctype1,
            'user':user_data,
            'sorted_by': '',

        }


    return render_to_response('scholarship/fin_dash.html', context_list, context)
