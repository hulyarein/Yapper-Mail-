from django import forms
from django.contrib.auth.models import User
from landing.models import Profile
from django.contrib.auth.hashers import check_password

class ChangeNameForm(forms.ModelForm):
    # Fields from the User model
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'firstName'
        }),
        required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'lastName'
        }),
        required=True
    )

    pass_verification = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'passVerify'
        }),
        required=True
    )

    class Meta:
        model = Profile  # Only fields from the Profile model here
        fields = ['middle_name']  # Adjust based on your Profile model

        widgets = {
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'middleName'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract user instance from kwargs
        super().__init__(*args, **kwargs)

        if user:
            # Populate User fields if user exists
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

            # Populate Profile fields if a profile exists
            profile = Profile.objects.filter(user=user).first()
            if profile:
                self.fields['middle_name'].initial = profile.middle_name

    def save(self, commit=True):
        user = self.instance.user  # Get the associated User instance
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()  # Save User data

        profile = super().save(commit=False)  # Save Profile data
        if commit:
            profile.save()
        return profile

class ChangeHomeAddressForm(forms.ModelForm):
    pass_verification = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'passVerify'
        }),
        required=True
    )

    class Meta:
        model = Profile
        fields = ['home_address']

        widgets = {
            'home_address': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'homeAddress'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        profile = Profile.objects.filter(user=user).first()
        if profile:
            self.fields['home_address'].initial = profile.home_address

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile


class ChangeWorkAddressForm(forms.ModelForm):
    pass_verification = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'passVerify'
        }),
        required=True
    )

    class Meta:
        model = Profile
        fields = ['work_address']

        widgets = {
            'work_address': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'workAddress'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        profile = Profile.objects.filter(user=user).first()
        if profile:
            self.fields['work_address'].initial = profile.work_address

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile

class ChangeBirthdayForm(forms.ModelForm):
    pass_verification = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'passVerify'
        }),
        required=True
    )

    class Meta:
        model = Profile
        fields = ['birthday']

        widgets = {
            'birthday': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'birthday',
                'type': 'date'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        profile = Profile.objects.filter(user=user).first()
        if profile:
            self.fields['birthday'].initial = profile.birthday

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile

class ChangeGenderForm(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('PNS', 'Prefer not to say'),
            ('Other', 'Other')
        ],
        widget=forms.RadioSelect,
        required=True
    )
    other_gender = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify if "Other"'})
    )
    pass_verification = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'passVerify',
            'placeholder': 'Password Verification'
        }),
        required=True
    )

    class Meta:
        model = Profile
        fields = ['gender']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        profile = Profile.objects.filter(user=user).first()
        
        # Set default gender if none exists
        if profile and not profile.gender.strip():  # Checking for empty or whitespace-only gender
            self.fields['gender'].initial = 'PNS'  # Default to 'Prefer not to say'
        else:
            self.fields['gender'].initial = profile.gender

    def save(self, commit=True):
        profile = super().save(commit=False)
        # Assign the specified gender
        profile.gender = self.cleaned_data['gender']
        if commit:
            profile.save()
        return profile

class ChangePasswordForm(forms.Form):
    pass_verification = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'passVerify'
        }),
        required=True,
        label="Current Password"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'newPass'
        }),
        required=True,
        label="New Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'confirmPass'
        }),
        required=True,
        label="Confirm New Password"
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_pass_verification(self):
        pass_verification = self.cleaned_data.get('pass_verification')
        if not check_password(pass_verification, self.user.password):
            raise forms.ValidationError("Current password is incorrect.")
        return pass_verification

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")
        
        return cleaned_data