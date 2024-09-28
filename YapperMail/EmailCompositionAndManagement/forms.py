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
