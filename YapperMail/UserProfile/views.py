from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from landing.models import Profile
from landing.models import CustomUser
from django.contrib.auth.decorators import login_required
from .forms import ChangeNameForm, ChangeHomeAddressForm, ChangeWorkAddressForm, ChangeBirthdayForm, ChangeGenderForm, ChangePasswordForm, ChangePhoneNumberForm
from django.contrib import messages
from django.contrib.auth import authenticate, update_session_auth_hash, logout
from django.templatetags.static import static

@login_required
def profilePage(request):
    # profile = get_object_or_404(Profile, user=request.user)
    user = request.user

    if request.method == "POST":
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']
            user.save(update_fields=['profile_picture'])
            return JsonResponse({'success': True}, status=200)

        # Handle profile picture removal
        elif request.POST.get('remove_photo') == "1":
            user.profile_picture = None
            user.save(update_fields=['profile_picture'])
            return JsonResponse({'success': True}, status=200)

        elif request.POST.get('delete_account') == "1":
            # Validate password for delete confirmation
            user = authenticate(username=user.username, password=request.POST.get('password'))
            if user is not None:
                user.delete()
                logout(request)  # Log out the user after deletion
                return JsonResponse({'success': True, 'message': 'Account deleted successfully.'}, status=200)
            else:
                return JsonResponse({'success': False, 'error': 'Invalid password. Please try again.'}, status=400)
    
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)
        
    profilepic = user.profile_picture.url if user.profile_picture else static('images/default_profile.jpg')

    context = {
        'profilepic': profilepic,
        'first_name': ' '.join(word.capitalize() for word in user.first_name.split()),
        'middle_name': ' '.join(word.capitalize() for word in user.middle_name.split())[:1] + "." if user.middle_name != ' ' or '' else "",
        'last_name': ' '.join(word.capitalize() for word in user.last_name.split()),
        'phone_number': user.pnumber,
        'birthday': (user.birthday, "Not specified") [user.birthday == None], 
        'gender': ("Prefer not to say",user.gender) [user.gender != "PNS"],
        'email_address': user.email,
        'home_address': (user.home_address, "Not specified") [user.home_address == ""],
        'work_address': (user.work_address, "Not specified") [user.work_address == ""]
    }

    return render(request, "profilePage.html", context)

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate

@login_required
def changeName(request):
    user = request.user  # Use the authenticated user directly

    if request.method == 'POST':
        form = ChangeNameForm(request.POST, user=user)

        if form.is_valid():
            # Extract the password for authentication
            password = form.cleaned_data['pass_verification']
            if authenticate(username=user.username, password=password):
                # Update user fields
                user.first_name = form.cleaned_data['first_name']
                user.middle_name = form.cleaned_data['middle_name']
                user.last_name = form.cleaned_data['last_name']
                user.save(update_fields=['first_name', 'middle_name', 'last_name'])

                return JsonResponse({'success': True}, status=200)  # Send a success response
            else:
                return JsonResponse({'success': False, 'error': 'Invalid password. Please try again.'}, status=400)
        else:
            # Collect and return form errors
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)

    else:
        # Prepopulate form with user's current data
        initial_data = {
            'first_name': user.first_name.title() if user.first_name else "",
            'middle_name': user.middle_name.title() if user.middle_name else "",
            'last_name': user.last_name.title() if user.last_name else "",
        }
        form = ChangeNameForm(initial=initial_data, user=user)
        return render(request, 'nameChange.html', {'form': form})

@login_required
def changeBday(request):
    user = request.user

    if request.method == 'POST':
        form = ChangeBirthdayForm(request.POST, user=user)

        if form.is_valid():
            password = form.cleaned_data['pass_verification']
            if authenticate(username=user.username, password=password):
                # update changes murag git commit
                user.birthday = form.cleaned_data['birthday']
                # confirm changes murag git push hahahaha
                user.save(update_fields=['birthday'])

                return JsonResponse({'success': True})  # Send a success response

            else:
                return JsonResponse({'success': False, 'error': 'Invalid password please try again.'}, status=400)
        else:
            errors = form.errors.as_json()  
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = ChangeBirthdayForm(initial={
            'birthday': user.birthday
        }, user=user)

    return render(request, 'bdayChange.html', {'form': form})

@login_required
def changeGender(request):
    user = request.user

    if request.method == 'POST':
        form = ChangeGenderForm(request.POST, user=user)
        
        if form.is_valid():
            password = form.cleaned_data['pass_verification']
            if authenticate(username=user.username, password=password):
                # Save the new gender information
                user.gender = form.cleaned_data['gender']
                if form.cleaned_data['gender'] == 'Other':
                    user.gender = form.cleaned_data['other_gender']  # Use custom gender if "Other" selected
                user.save(update_fields=['gender'])

                return JsonResponse({'success': True})  # Send success response

            else:
                return JsonResponse({'success': False, 'error': 'Invalid password, please try again.'}, status=400)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = ChangeGenderForm(initial={
            'gender': user.gender
        }, user=user)

    return render(request, 'genderChange.html', {'form': form})

@login_required
def changeNumber(request):
    user = request.user

    if request.method == 'POST':
        form = ChangePhoneNumberForm(request.POST, user=user.user)

        if form.is_valid():
            password = form.cleaned_data['pass_verification']
            if authenticate(username=user.username, password=password):
                # update changes murag git commit
                user.pnumber = form.cleaned_data['pnumber']
                # confirm changes murag git push hahahaha
                user.save(update_fields=['pnumber'])

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid password please try again.'}, status=400)
        else:
            errors = form.errors.as_json()  
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = ChangePhoneNumberForm(initial={
            'phone_number': user.pnumber
        }, user=user)

    return render(request, "numberChange.html", {'form': form})

def changeWork(request):
    user = request.user

    if request.method == 'POST':
        form = ChangeWorkAddressForm(request.POST, user=user.user)

        if form.is_valid():
            password = form.cleaned_data['pass_verification']
            if authenticate(username=user.username, password=password):
                # update changes murag git commit
                user.work_address = form.cleaned_data['work_address']
                # confirm changes murag git push hahahaha
                user.save(update_fields=['work_address'])

                return JsonResponse({'success': True})  # Send a success response

            else:
                return JsonResponse({'success': False, 'error': 'Invalid password please try again.'}, status=400)
        else:
            errors = form.errors.as_json()  
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = ChangeWorkAddressForm(initial={
            'work_address': user.work_address
        }, user=user)

    return render(request, 'workChange.html', {'form': form})

@login_required
def changeHome(request):
    user = request.user

    if request.method == 'POST':
        form = ChangeHomeAddressForm(request.POST, user=user.user)

        if form.is_valid():
            password = form.cleaned_data['pass_verification']
            if authenticate(username=user.username, password=password):
                # update changes murag git commit
                user.home_address = form.cleaned_data['home_address']
                # confirm changes murag git push hahahaha
                user.save(update_fields=['home_address'])

                return JsonResponse({'success': True})  # Send a success response

            else:
                return JsonResponse({'success': False, 'error': 'Invalid password please try again.'}, status=400)
        else:
            errors = form.errors.as_json()  
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = ChangeHomeAddressForm(initial={
            'home_address': user.home_address
        }, user=user)

    return render(request, 'homeChange.html', {'form': form})

@login_required
def changePassword(request):
    user = request.user

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=user)

        if form.is_valid():
            # Change the user's password
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()

            # Update the session hash to prevent logout
            update_session_auth_hash(request, user)
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = ChangePasswordForm(user=user)

    return render(request, 'passwordChange.html', {'form': form})
