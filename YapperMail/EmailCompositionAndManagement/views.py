from django.shortcuts import render,get_object_or_404,redirect
from .forms import EmailComposeForm,ReplyComposeForm,EditEmailForm,EditReplyForm
from .models import Email,EmailFiles,TemporaryUser
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def email_composition(request):
    error_message = False
    if request.method == "POST":
        form = EmailComposeForm(request.POST,request.FILES)
        if form.is_valid():
            toUser = form.cleaned_data['toUser']
            subject = form.cleaned_data['subject']
            description = form.cleaned_data['description']


            try:
                fromUser = TemporaryUser.objects.get(id = 1)
                toUserDatabase = TemporaryUser.objects.get(userEmail = toUser)
                email = Email(
                    fromUser=fromUser,
                    toUser=toUserDatabase,
                    subject=subject,
                    content=description
                )
                email.save()

                uploaded_files = request.FILES.getlist('file')
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        email_file = EmailFiles(
                            fromUser=fromUser,
                            toUser=toUserDatabase,
                            emailId=email, 
                            file=uploaded_file
                        )
                        email_file.save()  
                else:
                    print("No files were uploaded.")

                return redirect('email_composition')
            except ObjectDoesNotExist:
                error_message = True
        else:
            print("Not working")
            print(form.errors)

    else:
        form = EmailComposeForm()

    return render(request,"composeEmail.html",{'form':form,"errormessage":error_message})


def email_sent_view(request):
    if request.method == "POST":
        form = ReplyComposeForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data['message']
    else:
        form = ReplyComposeForm()

        
    return render(request,"emailSentView.html",{'form':form})

def email_reply_view(request):
    if request.method == "POST":
        form = ReplyComposeForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data['message']
    else:
        form = ReplyComposeForm()

        
    return render(request,"emailReceiveView.html",{'form':form})

def edit_email(request):
    if request.method == "POST":
        form = EditEmailForm(request.POST)
        if form.is_valid():
            toUser = form.cleaned_data['toUser']
            subject = form.cleaned_data['subject']

    else:
        form = EditEmailForm()

    return render(request,"editEmail.html",{'form':form})

def edit_reply(request):
    if request.method == "POST":
        form = EditReplyForm(request.POST)
        if form.is_valid():
            pass

    else:
        form = EditReplyForm()

    return render(request,"editReply.html",{'form':form})

