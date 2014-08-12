from django.shortcuts import render
# FOR TESTING
from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import Adoption


# Create your views here.

def index(request):
    #TODO: Currently Not Used. TemplateView is used instead.
    return render(request, 'facade/index.html', {})
    
    
    
@receiver(post_save, sender=Adoption)
def print_signal(sender, **kawrgs):
    print("Adoption was saved.")
    
    