from django.shortcuts import render
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
from django import forms
import requests
import json
import datetime


class DatePickerForm(forms.Form):
    day = forms.DateField(initial=datetime.date.today)

# Create your views here.
def index(request):
    #GET https://team02-rof.interopland.com/new-hope-services/fhir/Patient?name=Ben&_pretty=true
    BASE_URL = 'https://team02-rof.interopland.com/new-hope-services/fhir/Patient'
    msg = ""
    if request.method == 'POST':
        params = {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'phone': request.POST['phone'],
            '_pretty': 'true'}
        print(f"request.POST = {request.POST}")
        response = requests.get(BASE_URL, params = params,
                                auth=('mihin_hapi_fhir', 'cLQgfFT2oAgdzpXxA6jxRQxjZJSC5EurTwWx'))
        print(f"response = {response}")
        print(f"response.content = {response.text}")
        #try:
        msg = json.dumps(response.json(), indent=4, sort_keys=True)
        #except:
        #    msg = response.text
    return render(request, 'patient_search.html', {
        'msg': msg
    })
    #return HttpResponse("Hello, world. You're at the polls index.")

def slot_search(request):
    #GET https://team02-rof.interopland.com/new-hope-services/fhir/Patient?name=Ben&_pretty=true
    BASE_URL = 'https://team02-rof.interopland.com/new-hope-services/fhir/Slot'
    msg = ""
    if request.method == 'POST':
        form = DatePickerForm(request.POST)
        if form.is_valid():
            #Do Query
            print(f"request.POST = {request.POST}")
            start_date = datetime.datetime.strptime(request.POST['day'], '%Y-%m-%d')
            print(f"start_date = {start_date}")
            tomorrow_date = start_date + datetime.timedelta(days=1)
            params = {'start':[
                f'ge{start_date.replace(microsecond=0).isoformat()}',
                f'le{tomorrow_date.replace(microsecond=0).isoformat()}'
            ]}
            print(f"tomorrow_date = {tomorrow_date}")
            response = requests.get(BASE_URL, params = params,
                                auth=('mihin_hapi_fhir', 'cLQgfFT2oAgdzpXxA6jxRQxjZJSC5EurTwWx'))
        print(f"response = {response}")
        print(f"response.content = {response.text}")
        #try:
        msg = json.dumps(response.json(), indent=4, sort_keys=True)
        #except:
        #    msg = response.text
    else:
        form = DatePickerForm()

    return render(request, 'slot_search.html', {
        'form': form,
        'msg': msg
    })


# Create your views here.
def docSearch(request):
    #GET https://team02-rof.interopland.com/new-hope-services/fhir/Patient?name=Ben&_pretty=true
    #twzddba28GjsiSq!
    BASE_URL = 'https://team02-rof.interopland.com/new-hope-services/fhir/Patient'
    msg = ""
    if request.method == 'POST':
        params = {
            'name': request.POST['name'],
            'family': request.POST['email'],
            'phone': request.POST['phone'],
            '_pretty': 'true'
        }
        print(f"request.POST = {request.POST}")
        response = requests.get(BASE_URL, params = params,
                                auth=('mihin_hapi_fhir', 'cLQgfFT2oAgdzpXxA6jxRQxjZJSC5EurTwWx'))
        print(f"response = {response}")
        print(f"response.content = {response.text}")
        try:
            msg = json.dumps(response.json(), indent=4, sort_keys=True)
        except json.JSONDecodeError:
            msg = response.text
    return render(request, 'patient_search.html', {
        'msg': msg
    })
    #return HttpResponse("Hello, world. You're at the polls index.")
