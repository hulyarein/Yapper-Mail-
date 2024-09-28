from django.shortcuts import render,get_object_or_404
from .forms import EmailComposeForm

# Create your views here.

def email_composition(request):
    if request.method == "POST":
        form = EmailComposeForm(request.POST)
        if form.is_valid():
            toUser = form.cleaned_data['toUser']
            subject = form.cleaned_data['subject']

    else:
        form = EmailComposeForm()

    return render(request,"composeEmail.html",{'form':form})

