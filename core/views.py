from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    #GET https://team02-rof.interopland.com/new-hope-services/fhir/Patient?name=Ben&_pretty=true
    if request.method == 'POST':
        print(f"request.POST = {request.POST}")
        
    return render(request, 'patient_search.html', {
        'data': None
    })
    #return HttpResponse("Hello, world. You're at the polls index.")
