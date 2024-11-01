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

def compose_email_details(request):
    if request.method == 'POST':
        try:
            list_members = request.POST.get('listMembers', None)  # Get listMembers from POST data
            subject = request.POST.get('subject', None)
            description = request.POST.get('description', None)

            for email in list_members:
                if not User.objects.get(email=email).exists():
                    return JsonResponse({"message": "Some Users do not exist"}, status=201)
            
            team_email = TeamEmail.objects.create(
                fromUser=request.user,
                subject=subject,
                content=description
            )

            # Add the sender as an admin user
            team_email.adminUsers.add(request.user)

            # Add other users as member users
            for email in list_members:
                user_now = User.objects.get(email=email)
                if user_now != request.user:
                    team_email.memberUsers.add(user_now)


            uploaded_files = request.FILES.getlist('file')  # Get the list of uploaded files
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    email_file = TeamEmailFiles(
                        emailId=team_email,  # Link the file to the email created
                        file=uploaded_file
                    )
                    email_file.save()  # Save the file record

            return JsonResponse({"message": "Email details saved successfully"}, status=201)
    

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    return JsonResponse({"error": "Invalid request method"}, status=405)
