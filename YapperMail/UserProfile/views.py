from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.
def profilePage(request):
    session_check = checkSession(request)
    if isinstance(session_check, HttpResponse):
        return session_check

    return render(request, "profilePage.html")

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
