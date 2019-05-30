from django.shortcuts import render
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
import requests
import json


# Create your views here.
def index(request):
    #GET https://team02-rof.interopland.com/new-hope-services/fhir/Patient?name=Ben&_pretty=true
    #twzddba28GjsiSq!
    BASE_URL = 'https://team02-rof.interopland.com/new-hope-services/fhir/Patient'
    msg = ""
    if request.method == 'POST':
        params = {'name': request.POST['fname'], '_pretty': 'true'}
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
