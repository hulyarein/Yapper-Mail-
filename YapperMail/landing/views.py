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
from django.views.decorators.csrf import csrf_exempt
from notifications_app.models import *
from EmailCompositionAndManagement.models import *
import datetime
from .forms import EmailSearchForm
from django.db.models import Q

# Create your views here.

def search_emails(request):
    query = request.GET.get('search_query', '')
    results = []
    
    if query:
        results = Email.objects.filter(
            Q(subject__icontains=query) |
            Q(content__icontains=query) |
            Q(fromUser__username__icontains=query)
        )

    usermeid = request.user.id
    context = {
        'usermeid': usermeid,
        'results': results, 
        'query': query
    }
    
    form = EmailSearchForm()
    return render(request, 'registration/home.html', context)

@login_required
def email_calendar(request):
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)

    emails = Email.objects.filter(
        toUser=request.user,
        date_sent__gte=seven_days_ago,
        date_sent__lte=today
    ).order_by('date_sent')

    email_blocks = {
        'Mon': {},
        'Tue': {},
        'Wed': {},
        'Thu': {},
        'Fri': {},
        'Sat': {},
        'Sun': {},
    }

    for email in emails:
        email_datetime = email.date_sent
        day_of_week = email_datetime.strftime('%a') 
        hour_of_day = email_datetime.hour

        if day_of_week not in email_blocks:
            continue 

        if hour_of_day not in email_blocks[day_of_week]:
            email_blocks[day_of_week][hour_of_day] = []

        email_blocks[day_of_week][hour_of_day].append({
            'subject': email.subject,
            'content': email.content,
            'time': email_datetime.strftime('%H:%M')
        })

    return JsonResponse(email_blocks)

@login_required
def landing(request):
    return render (request, 'registration/landing.html')

def home(request):
    emails = Email.objects.filter(toUser=request.user).order_by('-date_sent') 
    plans = Email.objects.filter(toUser=request.user).order_by('-date_sent')[:1]
    notifications = Notification.objects.filter(to_user=request.user).order_by('-created_at')[:10]
    usermeid = request.user.id

    notif_read = Notification.objects.filter(is_read=False)
    
    context = {
        'usermeid': usermeid,
        'emails': emails,
        'plans': plans,
        'notifications' : notifications,
        'are_read' : True if len(notif_read) == 0 else False
    }

    return render(request, 'registration/home.html', context)  

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


def loginForm(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  
        
        else:
            print("Invalid form submission")
            return HttpResponse("Invalid login details. Please try again.")
    else:
        form = AuthenticationForm()
        print("Displaying login form")

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

                return JsonResponse({"redirect_url": "/home/"}, status=200)
            else:
                return JsonResponse({"message": "User not found for this phone number"}, status=404)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)

    return JsonResponse({"message": "Invalid request method"}, status=405)



def send_otp(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        try:
            verification = auth.start_phone_number_verification(phone_number)
            request.session['verification_id'] = verification.verification_id
            request.session['phone_number'] = phone_number
            return redirect('verify_otp')  
        except Exception as e:
            return render(request, 'enternumber.html', {'error': str(e)})
    return render(request, 'registration/enternumber.html')

def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            try:
                user = User.objects.get(username=username)  
                user.password = make_password(new_password)  
                user.save()
                messages.success(request, 'Your password has been reset successfully!')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'registration/resetpassword.html')

@csrf_exempt
def email_view(request):
    if request.method == 'POST':
        email_data = json.loads(request.body)
        request.session['email_data'] = email_data 
        print('Session Data:', request.session.get('email_data'))
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

def receive_view(request):
    email_data = request.session.get('email_data', None)  
    if email_data:
        return render(request, 'EmailSentView.html', {'email_data': email_data})
    return JsonResponse({'error': 'No email data found'}, status=404)

def retrieve_email_view(request):
    email_data = request.session.get('email_data', None) 
    print('Retrieving Session Data:', email_data)
    if email_data:
        return JsonResponse({'email_data': email_data})
    return JsonResponse({'error': 'No email data found'}, status=404)