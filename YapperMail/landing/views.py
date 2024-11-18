from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from landing.forms import CustomUserCreationForm 
from django.http import HttpResponse, JsonResponse
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
    return render(request, 'registration/home.html', {'emails': emails, 'plans': plans})  

def email_list(request):
    return render (request, 'emailList.html')

def profile(request):
    return render (request, 'profilePage.html')

def enterpnumber(request):
    return render (request, 'registration/enternumber.html')

def signupForm(request):
    if request.method == "POST":
        
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True  
            user.save()

            print("Successfully Signed up {user.username}")

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

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        verification_id = request.session.get('verification_id')

        try:
            # Confirm the OTP
            auth.verify_phone_number_otp(verification_id, otp)
            return redirect('reset_password')  # Redirect to password reset page
        except Exception as e:
            return render(request, 'registration/verifyotp.html', {'error': str(e)})
    return render(request, 'registration/verifyotp.html')


# def reset_password(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('confirm_password')

#         # Check if passwords match
#         if new_password == confirm_password:
#             try:
#                 user = User.objects.get(username=username)  # Retrieve user by username
#                 form = SetPasswordForm(user=user, data={'new_password1': new_password, 'new_password2': confirm_password})

#                 if form.is_valid():
#                     user.password = make_password(new_password)  # Hash the new password
#                     user.save()
#                     messages.success(request, 'Your password has been reset successfully!')
#                     return redirect('login')  # Redirect to login or success page
#                 else:
#                     return render(request, 'registration/resetpassword.html', {'form': form})

#             except User.DoesNotExist:
#                 return render(request, 'registration/resetpassword.html', {'error': 'User not found.'})
#         else:
#             return render(request, 'registration/resetpassword.html', {'error': 'Passwords do not match.'})

#     return render(request, 'registration/resetpassword.html')

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