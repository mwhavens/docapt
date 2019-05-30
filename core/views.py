from django.shortcuts import render
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
import requests
import json

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


# Create your views here.
def index(request):
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
