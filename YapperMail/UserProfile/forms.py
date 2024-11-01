from django import forms
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'firstName'
            }),
            'middle_initial': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'middleInitial'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'lastName'
            }),
            'pass_verification': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'passVerify'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user instance from kwargs
        super().__init__(*args, **kwargs)

        # If user exists, set the placeholders dynamically
        if user:
            self.fields['first_name'].widget.attrs['value'] = user.first_name
            self.fields['last_name'].widget.attrs['value'] = user.last_name
