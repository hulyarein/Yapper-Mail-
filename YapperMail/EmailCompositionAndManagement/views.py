from django.shortcuts import render,get_object_or_404

# Create your views here.

def email_composition(request):
    return render(request,"composeEmail.html")

