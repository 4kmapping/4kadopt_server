from django.shortcuts import render
# FOR TESTING
from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import Adoption
from django.http import HttpResponse, HttpResponseNotAllowed
from django.http import HttpResponseBadRequest

# Create your views here.

def index(request):
    #TODO: Currently Not Used. TemplateView is used instead.
    return render(request, 'facade/index.html', {})
    
    
'''    
@receiver(post_save, sender=Adoption)
def print_signal(sender, **kawrgs):
    print("Adoption was saved.")
'''    
    
    
def cleanup_adoptions(request):
    if request.method == 'GET':
        return render(request, 'facade/cleanup.html', {}) 
    
    elif request.method == 'POST' and request.user.is_superuser:
        if request.POST.get('command', None):
            cmd = request.POST.get('command')
            if cmd == 'CLEARUP-ADOPTIONS':
                Adoption.objects.filter(targetyear__gte='2015').delete()
                return HttpResponse('Deleted all adoptions.')
            else:
                print 'wrong command.'
                mssg = 'You typed a wrong command.'
                return HttpResponseBadRequest(mssg)
    else:
        mssg = "The HTTP method is not supported or you don't have a privilege."
        return HttpResponseBadRequest(mssg)


def download(request):
    return render(request, 'facade/download.html', {})
    
            
                