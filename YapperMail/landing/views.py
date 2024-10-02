from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from landing.forms import CustomUserCreationForm 

# Create your views here.
@login_required
def landing(request):
    return render (request, 'registration/landing.html')

def signupForm(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('landing:login') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {"form": form})

def loginForm(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('landing') 
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {"form": form})
