from django.shortcuts import render,get_object_or_404,redirect
from .forms import EmailComposeForm,ReplyComposeForm,EditEmailForm,EditReplyForm
from .models import Email,EmailFiles,TemporaryUser
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, Http404
import os
from urllib.parse import unquote

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

    
    getEmail = Email.objects.get(id = 6)

    getFiles = EmailFiles.objects.filter(emailId = getEmail)
        
    return render(request,"emailSentView.html",{'form':form,'emailCont':getEmail,'filesCont':getFiles})

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



BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIRECTORY = os.path.join(BASE_DIR, "")

def download_file(request, filename):
    filename = unquote(filename)

    file_path = os.path.normpath(os.path.join(UPLOAD_DIRECTORY, filename))

    print("Requested filename:", filename)
    print("Full file path:", file_path)
    print("UPLOAD_DIRECTORY:", UPLOAD_DIRECTORY)

    if not file_path.startswith(os.path.abspath(UPLOAD_DIRECTORY)):
        raise Http404("Invalid file path")

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        raise Http404(f"File not found: {filename}")

