from django import forms
from landing.models import CustomUser as User
from landing.models import Profile
from django.contrib.auth.hashers import check_password
from datetime import date
from django.core.exceptions import ValidationError

class ChangeNameForm(forms.ModelForm):
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
    middle_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'middleName'
        }),
        required=False  # Adjust based on your requirements
    )
    pass_verification = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'passVerify'
        }),
        required=True
    )

    class Meta:
        model = User 
        fields = ['first_name', 'last_name', 'middle_name']  # Ensure these fields exist in User

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract user instance from kwargs
        super().__init__(*args, **kwargs)

        if user:
            # Populate User fields if user exists
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['middle_name'].initial = getattr(user, 'middle_name', '')  # Use getattr for custom fields

    def save(self, commit=True):
        user = self.instance  # Since the form is tied directly to User
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.middle_name = self.cleaned_data.get('middle_name', '')  # Optional field

        if commit:
            user.save()
        return user
    
class ChangeHomeAddressForm(forms.ModelForm):
    home_address = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'homeAddress'
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
        model = User
        fields = ['home_address']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['home_address'].initial = user.home_address
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    
class ChangeWorkAddressForm(forms.ModelForm):
    work_address = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'workAddress'
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
        model = User
        fields = ['work_address']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['work_address'].initial = user.work_address
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    
class ChangeBirthdayForm(forms.ModelForm):
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'birthday',
            'type': 'date'
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
        model = User
        fields = ['birthday']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['birthday'].initial = user.birthday
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    
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
        model = User
        fields = ['gender']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            if user.gender in ['Male', 'Female', 'PNS']:
                self.fields['gender'].initial = user.gender
            else:
                self.fields['gender'].initial = 'Other'
                self.fields['other_gender'].initial = user.gender

    def save(self, commit=True):
        user = self.instance
        gender = self.cleaned_data['gender']
        user.gender = self.cleaned_data['other_gender'] if gender == 'Other' else gender

        if commit:
            user.save()
        return user

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

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password'])
        if commit:
            self.user.save()
        return self.user

class ChangePhoneNumberForm(forms.ModelForm):
    pass_verification = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'passVerify'
        }),
        required=True
    )

    class Meta:
        model = User
        fields = ['pnumber']

        widgets = {
            'pnumber': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'pnumber'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['pnumber'].initial = user.pnumber

    def save(self, commit=True):
        user = self.instance
        user.pnumber = self.cleaned_data['pnumber']

        if commit:
            user.save()
        return user



# class ChangeHomeAddressForm(forms.ModelForm):
#     pass_verification = forms.CharField(
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'id': 'passVerify'
#         }),
#         required=True
#     )

#     class Meta:
#         model = Profile
#         fields = ['home_address']

#         widgets = {
#             'home_address': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'homeAddress'
#             })
#         }

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)

#         profile = Profile.objects.filter(user=user).first()
#         if profile:
#             self.fields['home_address'].initial = profile.home_address

#     def save(self, commit=True):
#         profile = super().save(commit=False)
#         if commit:
#             profile.save()
#         return profile


# class ChangeWorkAddressForm(forms.ModelForm):
#     pass_verification = forms.CharField(
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'id': 'passVerify'
#         }),
#         required=True
#     )

#     class Meta:
#         model = Profile
#         fields = ['work_address']

#         widgets = {
#             'work_address': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'workAddress'
#             })
#         }

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)

#         profile = Profile.objects.filter(user=user).first()
#         if profile:
#             self.fields['work_address'].initial = profile.work_address

#     def save(self, commit=True):
#         profile = super().save(commit=False)
#         if commit:
#             profile.save()
#         return profile

# class ChangeBirthdayForm(forms.ModelForm):
#     pass_verification = forms.CharField(
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'id': 'passVerify'
#         }),
#         required=True
#     )

#     class Meta:
#         model = Profile
#         fields = ['birthday']

#         widgets = {
#             'birthday': forms.DateInput(attrs={
#                 'class': 'form-control',
#                 'id': 'birthday',
#                 'type': 'date'
#             })
#         }

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)

#         profile = Profile.objects.filter(user=user).first()
#         if profile:
#             self.fields['birthday'].initial = profile.birthday

#     def clean_birthday(self):
#         birthday = self.cleaned_data.get('birthday')
#         if birthday:
#             # Calculate age based on birthday
#             today = date.today()
#             age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
            
#             # Validate age
#             if age < 13:
#                 raise ValidationError("You must be at least 13 years old to set this date.")
        
#         return birthday

#     def save(self, commit=True):
#         profile = super().save(commit=False)
#         if commit:
#             profile.save()
#         return profile

# class ChangeGenderForm(forms.ModelForm):
#     gender = forms.ChoiceField(
#         choices=[
#             ('Male', 'Male'),
#             ('Female', 'Female'),
#             ('PNS', 'Prefer not to say'),
#             ('Other', 'Other')
#         ],
#         widget=forms.RadioSelect,
#         required=True
#     )
#     other_gender = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please specify if "Other"'})
#     )
#     pass_verification = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'id': 'passVerify',
#             'placeholder': 'Password Verification'
#         }),
#         required=True
#     )

#     class Meta:
#         model = Profile
#         fields = ['gender']

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)
#         profile = Profile.objects.filter(user=user).first()
        
#         if profile:
#             # Check if gender matches a predefined option or is a custom value
#             if profile.gender in ['Male', 'Female', 'PNS']:
#                 self.fields['gender'].initial = profile.gender
#             else:
#                 # If it's a custom gender, set 'Other' as the selected radio button
#                 self.fields['gender'].initial = 'Other'
#                 self.fields['other_gender'].initial = profile.gender  # Populate `other_gender` field with the custom value

#     def save(self, commit=True):
#         profile = super().save(commit=False)
#         # Assign the specified gender
#         profile.gender = self.cleaned_data['gender']
#         if commit:
#             profile.save()
#         return profile

# class ChangePasswordForm(forms.Form):
#     pass_verification = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'id': 'passVerify'
#         }),
#         required=True,
#         label="Current Password"
#     )
#     new_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'id': 'newPass'
#         }),
#         required=True,
#         label="New Password"
#     )
#     confirm_password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'form-control',
#             'id': 'confirmPass'
#         }),
#         required=True,
#         label="Confirm New Password"
#     )

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)

#     def clean_pass_verification(self):
#         pass_verification = self.cleaned_data.get('pass_verification')
#         if not check_password(pass_verification, self.user.password):
#             raise forms.ValidationError("Current password is incorrect.")
#         return pass_verification

#     def clean(self):
#         cleaned_data = super().clean()
#         new_password = cleaned_data.get('new_password')
#         confirm_password = cleaned_data.get('confirm_password')

#         if new_password and confirm_password and new_password != confirm_password:
#             raise forms.ValidationError("New passwords do not match.")
        
#         return cleaned_data
    
# class ChangePhoneNumberForm(forms.ModelForm):
#     pass_verification = forms.CharField(
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'id': 'passVerify'
#         }),
#         required=True
#     )

#     class Meta:
#         model = Profile
#         fields = ['pnumber']

#         widgets = {
#             'pnumber': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'pnumber'
#             })
#         }

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)

#         profile = Profile.objects.filter(user=user).first()
#         if profile:
#             self.fields['pnumber'].initial = profile.pnumber    

#     def save(self, commit=True):
#         profile = super().save(commit=False)
#         if commit:
#             profile.save()
#         return profile