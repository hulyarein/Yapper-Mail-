from django.shortcuts import render,get_object_or_404,redirect
from .forms import TeamEmailComposeForm,ReplyComposeForm,EditEmailForm,EditReplyForm,SearchForm
from .models import TeamEmail,TeamEmailFiles,TeamReply,TeamReplyFiles
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, Http404
import os
from urllib.parse import unquote
import json
from django.http import JsonResponse,HttpResponse
from django.db.models import Q


def team_email_composition(request,pk):
    error_message = False
    if request.method == "POST":
        form = TeamEmailComposeForm(request.POST,request.FILES)
        if form.is_valid():
            toUser = form.cleaned_data['toUser']
            subject = form.cleaned_data['subject']
            description = form.cleaned_data['description']


            try:
                fromUser = request.user
                toUserDatabase = User.objects.get(email = toUser)
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

                return redirect('emailListView')
            except ObjectDoesNotExist:
                error_message = True
        else:
            print("Not working")
            print(form.errors)

    else:
        form = TeamEmailComposeForm()

    #return render(request,"composeEmail.html",{'form':form,"errormessage":error_message})
    return render(request,"teamcomposeEmail.html",{'form':form})