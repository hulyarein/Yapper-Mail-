from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    fname = forms.CharField(max_length=30, required=True)
    lname = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    pnumber = forms.CharField(max_length=13, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'fname', 'lname', 'pnumber', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['fname']
        user.last_name = self.cleaned_data['lname']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  
        user.pnumber = self.cleaned_data['pnumber']  
        
        if commit:
            user.save()
        
        return user

class EmailSearchForm(forms.Form):
    search_query = forms.CharField(label='Search Emails', max_length=100)