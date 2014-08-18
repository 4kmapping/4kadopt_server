import json
from django.shortcuts import render
from api.models import Adoption
from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required


def ozlist(request):
    if request.method == 'GET':
        query = request.GET['q'];
        res_json = {}
        if query == 'adopted':
            ozs = Adoption.objects.filter(is_adopted=True)
            res_json['count'] = len(ozs)
            results = [] 
            for oz in ozs:
                print oz.worldid, oz.targetyear
                ozitem = {}
                ozitem['worldid'] = oz.worldid
                ozitem['targetyear'] = int(oz.targetyear)  
                results.append(ozitem)
            res_json['results'] = results
                 
        return HttpResponse(json.dumps(res_json))
        
    else:
        return HttpResponseNotAllowed(['GET'])


#@login_required(login_url='/admin/login/')
def ozstatus(request):
    if request.method == 'GET':
        status = 'na'
        if request.GET.get('wid', None):
            wid = request.GET['wid']
            ozs = Adoption.objects.filter(worldid=wid)
            if len(ozs) > 0:
                status = ozs[0].is_adopted
        return HttpResponse(status)
    elif request.method == 'POST':
        wid = request.POST.get('wid', None)
        tyear = request.POST.get('tyear', None)
        is_adopted = request.POST.get('adopted', None)
        if wid and tyear and is_adopted == 'true': # Adopting an oz
            adoptions = Adoption.objects.filter(worldid=wid, is_adopted=False)
            if len(adoptions) == 1:
                adoption = adoptions[0]
                adoption.targetyear = tyear
                adoption.is_adopted = True
                adoption.save()
            else:
                mssg = 'There is no oz that has been on hold'
                return HttpResponseBadRequest(mssg)
        
        elif wid and is_adopted == 'false': # locking an oz
            ozs = Adoption.objects.filter(worldid=wid)
            if len(ozs) == 0:
                adoption = Adoption()
                adoption.worldid = wid
                adoption.targetyear = int(tyear)
                adoption.is_adopted = False
                adoption.save()
            else:
                mssg = 'The requested oz has already adopted.'
                return HttpReponseBadRequest(mssg)            
        else:
            return HttpReponseBadRequest()
    elif request.method == 'DELETE':
        wid = request.POST.get('wid', None)
        # TODO: Check ownership
        adoptions = Adoption.objects.filter(worldid=wid)
        if len(adoptions) > 0:
            adoption = adoptions[0]
            adoption.delete()
            return HttpResponse('ok')
        else:
            mssg = 'There is no adopted oz to delete.'
            return HttpResonseBadRequest(mssg)
    else:
        mssg = 'The HTTP method is not supported'
        return HttpResponseBadRequest(mssg)
    