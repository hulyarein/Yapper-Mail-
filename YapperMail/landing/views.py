from django.shortcuts import render

# Create your views here.
def landing(request):
    return render (request, 'registration/landing.html')
