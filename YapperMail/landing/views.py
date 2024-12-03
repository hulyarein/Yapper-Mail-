from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from landing.forms import CustomUserCreationForm 
from landing.models import CustomUser
from django.http import HttpResponse, JsonResponse
import firebase_admin
from firebase_admin import auth
import json
import requests
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from EmailCompositionAndManagement.models import Email
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages


# Create your views here.
@login_required
def landing(request):
    return render (request, 'registration/landing.html')

def home(request):
    emails = Email.objects.filter(toUser=request.user).order_by('-date_sent') 
    plans = Email.objects.filter(toUser=request.user).order_by('-date_sent')[:1] # Fetch all event requests ordered by creation date
    # context = {
    #     'usermeid': request.user.id,  # or logic to get a specific user ID
    # }

    usermeid = request.user.id
    return render(request, 'registration/home.html', {'usermeid': usermeid, 'emails': emails, 'plans': plans})  

def email_list(request):
    return render (request, 'emailList.html')

def compose(request):
    return render (request, 'composeEmail.html')

def profile(request):
    return render (request, 'profilePage.html')

def enterpnumber(request):
    return render (request, 'registration/enternumber.html')

def signin_number(request):
    return render (request, 'registration/numbersignin.html')

def signupForm(request):
    print("re2uquest receicved")
    if request.method == "POST":
        
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_staff = True  
            user.save()

            print("Successfully Signed up {user.username}")

            return redirect('login') 
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
        print(form.errors)
    return render(request, 'registration/signup.html', {"form": form})

# def loginForm(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             print("Form is valid")
#             user = form.get_user()
#             auth_login(request, user)
#             # print("User is authenticated, redirecting to /landing/")
#             return redirect('home') 
#         else:
#             print("Invalid form submission")
#             return HttpResponse("Invalid login details. Please try again.")
#     else:
#         form = AuthenticationForm()
#         print("Displaying login form")
    
#     # ako gi change laine -ninin
#     return render(request, 'registration/login.html', {"form": form})
#     # return render(request, 'home', {"form": form})

def loginForm(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.get_user()
            auth_login(request, user)
            # Pass the user.id to the template after successful login
            return redirect('home')  # Redirect to the home page or another page
        
        else:
            print("Invalid form submission")
            return HttpResponse("Invalid login details. Please try again.")
    else:
        form = AuthenticationForm()
        print("Displaying login form")

    # Render the login form with the user_id context
    return render(request, 'registration/login.html', {"form": form})


if not firebase_admin._apps:
    firebase_admin.initialize_app()

def phone_login(request):
    if request.method == "POST":
        try:
            phone_number = request.POST.get('phone_number')
            parsed_number = phone_number.replace(" ", "")
            user = CustomUser.objects.filter(pnumber=parsed_number).first()

            if user:
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                # Return a JSON response with the redirect URL
                return JsonResponse({"redirect_url": "/home/"}, status=200)
            else:
                return JsonResponse({"message": "User not found for this phone number"}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)

    return JsonResponse({"message": "Invalid request method"}, status=405)



def send_otp(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        # Firebase phone verification - initiate OTP sending
        try:
            verification = auth.start_phone_number_verification(phone_number)
            request.session['verification_id'] = verification.verification_id
            request.session['phone_number'] = phone_number
            return redirect('verify_otp')  # Redirect to OTP input page
        except Exception as e:
            return render(request, 'enternumber.html', {'error': str(e)})
    return render(request, 'registration/enternumber.html')

def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if new_password == confirm_password:
            try:
                user = User.objects.get(username=username)  # Retrieve user by username
                user.password = make_password(new_password)  # Hash the new password
                user.save()
                messages.success(request, 'Your password has been reset successfully!')
                return redirect('login')  # Redirect to login page
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'registration/resetpassword.html')