from django.shortcuts import render
from django.http import HttpResponse
from requests.auth import HTTPBasicAuth
from django import forms
import requests
import json
import datetime
import fhirclient.models.bundle as bund
from django.shortcuts import redirect

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
            'phone': request.POST['phone'],
            #'phone': request.POST['phone'],
            '_pretty': 'true'}
        print(f"request.POST = {request.POST}")
        response = requests.get(BASE_URL, params = params,
                                auth=('mihin_hapi_fhir', 'cLQgfFT2oAgdzpXxA6jxRQxjZJSC5EurTwWx'))
        print(f"response = {response}")
        print(f"response.content = {response.text}")
        try:
            msg = json.dumps(response.json(), indent=4, sort_keys=True)
        except:
            msg = response.text
    return render(request, 'patient_search.html', {
        'msg': msg
    })
    #return HttpResponse("Hello, world. You're at the polls index.")


def fill_slot(request, slot_id):
    ROOT_URL = 'https://team02-rof.interopland.com/new-hope-services/fhir/Slot/'
    resp = requests.get(
        ROOT_URL + str(slot_id),
        auth=('mihin_hapi_fhir', 'cLQgfFT2oAgdzpXxA6jxRQxjZJSC5EurTwWx')
    )
    resp_text = resp.text
    resp_text = resp_text.replace("free", "busy")
    print(f"resp = {resp_text}")
    resp2 = requests.put(
        ROOT_URL + str(slot_id),
        data=resp_text,
        auth=('mihin_hapi_fhir', 'cLQgfFT2oAgdzpXxA6jxRQxjZJSC5EurTwWx')
    )
    print(f"resp2 = {resp2}")
    response = redirect('slotSearch')
    return response

    
def slot_search(request):
    #GET https://team02-rof.interopland.com/new-hope-services/fhir/Patient?name=Ben&_pretty=true
    BASE_URL = 'https://team02-rof.interopland.com/new-hope-services/fhir/Slot'
    ROOT_URL = 'https://team02-rof.interopland.com/new-hope-services/fhir/'
    msg = ""
    slots = []
    sched = {}
    provs = {}
    locs = {}
    ui_slots = []
    if request.method == 'POST':
        form = DatePickerForm(request.POST)
        if form.is_valid():
            #Do Query
            #print(f"request.POST = {request.POST}")
            start_date = datetime.datetime.strptime(request.POST['day'], '%Y-%m-%d')
            #print(f"start_date = {start_date}")
            tomorrow_date = start_date + datetime.timedelta(days=1)
            params = {
                'status': 'free',
                'start':[
                    f'ge{start_date.replace(microsecond=0).isoformat()}',
                    f'le{tomorrow_date.replace(microsecond=0).isoformat()}'
            ]}
            print(f"tomorrow_date = {tomorrow_date}")
            response = requests.get(BASE_URL, params = params,
                                auth=('mihin_hapi_fhir', 'cLQgfFT2oAgdzpXxA6jxRQxjZJSC5EurTwWx'))
            #print(f"response = {response}")
            #print(f"response.content = {response.text}")
            bundle = bund.Bundle(response.json())
            #print(f"bund = {bundle}")
            #print(f"bund_dict = {bundle.__dict__}")
            entries = bundle.entry
            for entry in entries:
                print(f"entry = {entry.resource.__dict__}")
                sdate = entry.resource.start.date
                sched_ref = entry.resource.schedule.reference
                print(f"sdate = {sdate}, sched_ref = {sched_ref}")
                slots.append((
                    entry.resource.start.date,
                    entry.resource.end.date,
                    entry.resource.schedule.reference,
                    entry.resource.id
                ))
                if sched_ref not in sched:
                    resp = requests.get(
                        ROOT_URL + sched_ref,
                        auth=('mihin_hapi_fhir', 'cLQgfFT2oAgdzpXxA6jxRQxjZJSC5EurTwWx')
                    )
                    print(f"resp = {resp.text}")
                    try:
                        sched[sched_ref] = resp.json()
                    except:
                        sched[sched_ref] = resp.text
            for sched_key, sched_val in sched.items():
                actors = sched_val['actor']
                prac_ref = None
                loc_ref = None
                for actor in actors:
                    print(f"actor = {actor}")
                    if actor['reference'].startswith('Location'):
                        loc_ref = actor['reference']
                    elif actor['reference'].startswith('Practitioner'):
                        prac_ref = actor['reference']
                    else:
                        print(f"Unknown actor reference: {actor.reference}")
                print(f"loc_ref = {loc_ref}, prac_ref = {prac_ref}")
                sched[sched_key] = (loc_ref, prac_ref)
                if loc_ref not in locs:
                    resp = requests.get(
                        ROOT_URL + loc_ref,
                        auth=('mihin_hapi_fhir', 'cLQgfFT2oAgdzpXxA6jxRQxjZJSC5EurTwWx')
                    )
                    print(f"resp = {resp.text}")
                    try:
                        locs[loc_ref] = resp.json()
                    except:
                        locs[loc_ref] = resp.text
                if prac_ref not in provs:
                    resp = requests.get(
                        ROOT_URL + prac_ref,
                        auth=('mihin_hapi_fhir', 'cLQgfFT2oAgdzpXxA6jxRQxjZJSC5EurTwWx')
                    )
                    print(f"resp = {resp.text}")
                    try:
                        provs[prac_ref] = resp.json()
                    except:
                        provs[prac_ref] = resp.text
                
                #print(f"entry = {entry.resource.__dict__}")
                #print(f"date = {entry.resource.start.date}")
                #reference
                #print(f"sched = {entry.resource.schedule.__dict__}")
            print(f"sched = {sched}")
            print(f"locs = {locs}")
            print(f"provs = {provs}")

        for slot in slots:
            print(f"slot[2] = {slot[2]}")
            print(f"sched = {sched}")
            s = sched[slot[2]]
            print(f"s = {s}")
            l = locs[s[0]]['name']
            p = provs[s[1]]['name'][0]
            print(f"l = {l}, p = {p}")
            p_name = f"{p['family']}, {p['given'][0]}"
            print(f"p_name = {p_name}")
            #print(f"loc = {locs[s[0]]}\nprac = {provs[s[1]]}")
            
            ui_slots.append([
                slot[0], slot[1],
                l, p_name,
                slot[3]
            ])
            #msg += f"\n{slot[0]}-{slot[1]}:{locs[
            
        try:
            msg = json.dumps(response.json(), indent=4, sort_keys=True)
        except:
            msg = response.text
    else:
        form = DatePickerForm()

    print(f"ui_slots = {ui_slots}")
    return render(request, 'slot_search.html', {
        'form': form,
        'ui_slots': ui_slots,
        'msg': msg
    })

#{locs[sched[0]]}

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
