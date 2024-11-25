from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from landing.models import Profile
from django.contrib.auth.decorators import login_required
from .forms import ChangeNameForm, ChangeHomeAddressForm, ChangeWorkAddressForm, ChangeBirthdayForm, ChangeGenderForm, ChangePasswordForm, ChangePhoneNumberForm
from django.contrib import messages
from django.contrib.auth import authenticate, update_session_auth_hash, logout

@login_required
def profilePage(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']
            profile.save(update_fields=['profile_picture'])
            return JsonResponse({'success': True}, status=200)

        # Handle profile picture removal
        elif request.POST.get('remove_photo') == "1":
            profile.profile_picture = None
            profile.save(update_fields=['profile_picture'])
            return JsonResponse({'success': True}, status=200)

        elif request.POST.get('delete_account') == "1":
            # Validate password for delete confirmation
            user = authenticate(username=profile.user.username, password=request.POST.get('password'))
            if user is not None:
                profile.user.delete()
                logout(request)  # Log out the user after deletion
                return JsonResponse({'success': True, 'message': 'Account deleted successfully.'}, status=200)
            else:
                return JsonResponse({'success': False, 'error': 'Invalid password. Please try again.'}, status=400)
    
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request.'}, status=400)
    

    context = {
        'profilepic': profile.profile_picture,
        'first_name': ' '.join(word.capitalize() for word in profile.user.first_name.split()),
        'middle_name': ' '.join(word.capitalize() for word in profile.middle_name.split())[:1] + "." if profile.middle_name else "",
        'last_name': ' '.join(word.capitalize() for word in profile.user.last_name.split()),
        'phone_number': profile.pnumber,
        'birthday': (profile.birthday, "Not specified") [profile.birthday == None], 
        'gender': ("Prefer not to say",profile.gender) [profile.gender != "PNS"],
        'email_address': profile.user.email,
        'home_address': (profile.home_address, "Not specified") [profile.home_address == ""],
        'work_address': (profile.work_address, "Not specified") [profile.work_address == ""]
    }

    return render(request, "profilePage.html", context)

@login_required
def changeName(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ChangeNameForm(request.POST, user=profile.user)
        
        if form.is_valid():
            # Extract the password for authentication
            password = form.cleaned_data['pass_verification']
            if authenticate(username=profile.user.username, password=password):
                profile.user.first_name = form.cleaned_data['first_name']
                profile.middle_name = form.cleaned_data['middle_name']
                profile.user.last_name = form.cleaned_data['last_name']
                profile.user.save(update_fields=['first_name', 'last_name'])
                profile.save(update_fields=['middle_name'])

                return JsonResponse({'success': True}, status=200)  # Send a success response
            else:
                return JsonResponse({'success': False, 'error': 'Invalid password please try again.'}, status=400)
        else:
            # Collect form errors and return them
            errors = form.errors.as_json()  # Get errors in JSON format
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        # Load the form with initial user data
        if profile.middle_name  == None:
            middle_name = ""
        else:
            middle_name = ' '.join(word.capitalize() for word in profile.middle_name.split())

        form = ChangeNameForm(initial={
            'first_name': ' '.join(word.capitalize() for word in profile.user.first_name.split()),
            'middle_name': middle_name,
            'last_name': ' '.join(word.capitalize() for word in profile.user.last_name.split())
        }, user=profile.user)

    return render(request, 'nameChange.html', {'form': form})

@login_required
def changeBday(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ChangeBirthdayForm(request.POST, user=profile.user)

        if form.is_valid():
            password = form.cleaned_data['pass_verification']
            if authenticate(username=profile.user.username, password=password):
                # update changes murag git commit
                profile.birthday = form.cleaned_data['birthday']
                # confirm changes murag git push hahahaha
                profile.save(update_fields=['birthday'])

                return JsonResponse({'success': True})  # Send a success response

            else:
                return JsonResponse({'success': False, 'error': 'Invalid password please try again.'}, status=400)
        else:
            errors = form.errors.as_json()  
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = ChangeBirthdayForm(initial={
            'birthday': profile.birthday
        }, user=profile.user)

    return render(request, 'bdayChange.html', {'form': form})

@login_required
def changeGender(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ChangeGenderForm(request.POST, user=profile.user)
        
        if form.is_valid():
            password = form.cleaned_data['pass_verification']
            if authenticate(username=profile.user.username, password=password):
                # Save the new gender information
                profile.gender = form.cleaned_data['gender']
                if form.cleaned_data['gender'] == 'Other':
                    profile.gender = form.cleaned_data['other_gender']  # Use custom gender if "Other" selected
                profile.save(update_fields=['gender'])

                return JsonResponse({'success': True})  # Send success response

            else:
                return JsonResponse({'success': False, 'error': 'Invalid password, please try again.'}, status=400)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = ChangeGenderForm(initial={
            'gender': profile.gender
        }, user=profile.user)

    return render(request, 'genderChange.html', {'form': form})

@login_required
def changeNumber(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ChangePhoneNumberForm(request.POST, user=profile.user)

        if form.is_valid():
            password = form.cleaned_data['pass_verification']
            if authenticate(username=profile.user.username, password=password):
                # update changes murag git commit
                profile.pnumber = form.cleaned_data['pnumber']
                # confirm changes murag git push hahahaha
                profile.save(update_fields=['pnumber'])

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid password please try again.'}, status=400)
        else:
            errors = form.errors.as_json()  
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = ChangePhoneNumberForm(initial={
            'phone_number': profile.pnumber
        }, user=profile.user)

    return render(request, "numberChange.html", {'form': form})

def changeWork(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ChangeWorkAddressForm(request.POST, user=profile.user)

        if form.is_valid():
            password = form.cleaned_data['pass_verification']
            if authenticate(username=profile.user.username, password=password):
                # update changes murag git commit
                profile.work_address = form.cleaned_data['work_address']
                # confirm changes murag git push hahahaha
                profile.save(update_fields=['work_address'])

                return JsonResponse({'success': True})  # Send a success response

            else:
                return JsonResponse({'success': False, 'error': 'Invalid password please try again.'}, status=400)
        else:
            errors = form.errors.as_json()  
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = ChangeWorkAddressForm(initial={
            'work_address': profile.work_address
        }, user=profile.user)

    return render(request, 'workChange.html', {'form': form})

@login_required
def changeHome(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ChangeHomeAddressForm(request.POST, user=profile.user)

        if form.is_valid():
            password = form.cleaned_data['pass_verification']
            if authenticate(username=profile.user.username, password=password):
                # update changes murag git commit
                profile.home_address = form.cleaned_data['home_address']
                # confirm changes murag git push hahahaha
                profile.save(update_fields=['home_address'])

                return JsonResponse({'success': True})  # Send a success response

            else:
                return JsonResponse({'success': False, 'error': 'Invalid password please try again.'}, status=400)
        else:
            errors = form.errors.as_json()  
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        form = ChangeHomeAddressForm(initial={
            'home_address': profile.home_address
        }, user=profile.user)

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
