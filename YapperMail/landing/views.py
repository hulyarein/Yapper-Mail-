from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from landing.forms import CustomUserCreationForm 
from django.http import HttpResponse


# Create your views here.
@login_required
def landing(request):
    return render (request, 'registration/landing.html')

def home(request):
    return render (request, 'registration/home.html')

def signupForm(request):
    if request.method == "POST":
        
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True  
            user.save()
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
        print(form.errors)
    return render(request, 'registration/signup.html', {"form": form})

def loginForm(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.get_user()
            auth_login(request, user)
            # print("User is authenticated, redirecting to /landing/")
            return redirect('home') 
        else:
            print("Invalid form submission")
            return HttpResponse("Invalid login details. Please try again.")
    else:
        form = AuthenticationForm()
        print("Displaying login form")
    
    # ako gi change laine -ninin
    return render(request, 'registration/login.html', {"form": form})
    # return render(request, 'home', {"form": form})
