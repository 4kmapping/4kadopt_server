from django.shortcuts import render

# Create your views here.

def index(request):
    #TODO: Currently Not Used. TemplateView is used instead.
    return render(request, 'facade/index.html', {})
