from django.http import HttpResponse
from django.db.models import Q
from django.core.exceptions import ValidationError

from models import Institute


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