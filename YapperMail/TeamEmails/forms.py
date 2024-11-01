from django import forms

class TeamEmailComposeForm(forms.Form):
    toUser = forms.EmailField(widget=forms.TextInput(attrs={
            'class': 'userToForm',
            'placeholder': 'Enter Userss here',
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
    
class TeamReplyComposeForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows':2,
            'columns':40,
            'class':'messageForm',
            'placeholder':'Enter reply here'
        })
    )

class TeamEditEmailForm(forms.Form):
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
    
class TeamEditReplyForm(forms.Form):
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows':20,
            'columns':40,
            'class': 'descriptionForm',
            'placeholder': 'Enter Description here',
        }))
    
class TeamSearchForm(forms.Form):
    searchContent = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'searchCont',
            'placeholder': 'Search',
        })
    )
