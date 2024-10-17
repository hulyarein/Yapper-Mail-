from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from landing.models import Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib import messages


@login_required
def profilePage(request):
    profile = get_object_or_404(Profile, user=request.user)

    first_name = profile.user.first_name
    last_name = profile.user.last_name
    #    birthday = profile.birthday
    #    gender = profile.gender

    phone_number = profile.pnumber
    email_address = profile.user.username

    # home = profile.home_address
    # work = profile.work_address

    context = {
        'profilepic': "yawa",

        'first_name': ' '.join(word.capitalize() for word in first_name.split()),
        'last_name': ' '.join(word.capitalize() for word in last_name.split()),
        # 'bday': bday
        # 'gender': gender

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

    return render(request, "profilePage.html", context)


@login_required
def changeName(request):
    user = request.user  # Get the current user

    if request.method == 'POST':
        form = ProfileForm(request.POST, user=user)  # Pass user to the form
        if form.is_valid():
            # something about unique constraints
            # naay better option aka overiding save function sa models
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save(update_fields=['first_name', 'last_name'])

            messages.success(request, 'Changes saved successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Load the form with initial user data
        form = ProfileForm(initial={
            'first_name': ' '.join(word.capitalize() for word in user.first_name.split()),
            'last_name': ' '.join(word.capitalize() for word in user.last_name.split())
        }, user=user)

    return render(request, 'nameChange.html', {'form': form})


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
