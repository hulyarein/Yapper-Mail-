from django import forms

class EmailComposeForm(forms.Form):
    toUser = forms.EmailField(widget=forms.TextInput(attrs={
            'class': 'userToForm',
            'placeholder': 'Enter User here',
        }))
    subject = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'subjectForm',
            'placeholder': 'Enter Subject here',
        }))
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows':10,
            'columns':40,
            'class': 'descriptionForm',
            'placeholder': 'Enter Description here',
        }))
    
class ReplyComposeForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows':2,
            'columns':40,
            'class':'messageForm',
            'placeholder':'Enter reply here'
        })
    )

class EditEmailForm(forms.Form):
    toUser = forms.EmailField(widget=forms.TextInput(attrs={
            'class': 'userToForm',
            'placeholder': 'Enter User here',
            'readonly':True
        }))
    subject = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'subjectForm',
            'placeholder': 'Enter Subject here',
        }))
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows':10,
            'columns':40,
            'class': 'descriptionForm',
            'placeholder': 'Enter Description here',
        }))
