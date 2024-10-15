from django.shortcuts import render,redirect
from django.http import HttpResponse
from landing.models import Profile

# Create your views here.
def profilePage(request):
    session_check = checkSession(request)
    if isinstance(session_check, HttpResponse):
        return session_check

    profile = Profile.objects.filter(user=request.user).first()

    first_name = profile.user.first_name
    last_name = profile.user.last_name
    #    birthday = profile.birthday
    #    gender = profile.gender

    phone_number = profile.pnumber
    email_address = profile.user.username

    # home = profile.home_address
    # work = profile.work_address
   
    context = {
        'first_name': ' '.join(word.capitalize() for word in first_name.split()),
        'last_name': ' '.join(word.capitalize() for word in last_name.split()),
        #'bday': bday
        #'gender': gender

        'phone_number': phone_number,
        'email_address': email_address + '@yapper.com'
        
        # 'home_address': home
        # 'work_address': work
    }
#    lastname
#    birthday
#    phonenumber
#    emailaddress
#    home
#    work


    return render(request, "profilePage.html",context)

def changeName(request):
    session_check = checkSession(request)
    if isinstance(session_check, HttpResponse):
        return session_check

    return render(request,"nameChange.html")

def changeBday(request):
    session_check = checkSession(request)
    if isinstance(session_check, HttpResponse):
        return session_check

    return render(request, "bdayChange.html")

def changeGender(request):
    session_check = checkSession(request)
    if isinstance(session_check, HttpResponse):
        return session_check

    return render(request, "genderChange.html")

def changeNumber(request):
    session_check = checkSession(request)
    if isinstance(session_check, HttpResponse):
        return session_check

    return render(request, "numberChange.html")

def changeEmail(request):
    session_check = checkSession(request)
    if isinstance(session_check, HttpResponse):
        return session_check

    return render(request, "emailChange.html")

def changeWork(request):
    session_check = checkSession(request)
    if isinstance(session_check, HttpResponse):
        return session_check

    return render(request, "workChange.html")

def changeHome(request):
    session_check = checkSession(request)
    if isinstance(session_check, HttpResponse):
        return session_check

    return render(request, "homeChange.html")

def checkSession(request):
    if not request.user.is_authenticated:
        return redirect('changeBday')
    return None
