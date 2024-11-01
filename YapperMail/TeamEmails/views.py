from django.shortcuts import render,get_object_or_404,redirect
from .forms import TeamEmailComposeForm,TeamReplyComposeForm,EditEmailForm,EditReplyForm,TeamSearchForm
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

            list_members = json.loads(list_members)

            for email in list_members:
                if not User.objects.filter(email=email).exists():
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

def team_emailListView(request):
    form = TeamSearchForm()

    #userVar = TemporaryUser.objects.get(id = 1)
    userVar = request.user
    emailsVar = TeamEmail.objects.filter(adminUsers=userVar)
    emailsVarMe = TeamEmail.objects.filter(memberUsers=userVar)

    combined_emails = emailsVar.union(emailsVarMe)
    return render(request,'TeamemailList.html',{'form':form,'emails':combined_emails,'LogUser':userVar})

def team_sentEmailList(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            if data.get('sentNum') == 2:
                #userVar = TemporaryUser.objects.get(id=1)
                userVar = request.user
                emailsVar = TeamEmail.objects.filter(adminUsers=userVar)

                email_data = [
                    {
                        "id": email.id,
                        "subject": email.subject,
                        "content": email.content,
                        "fromUser": email.fromUser.email,
                        "fromUserId": email.fromUser.id,
                        "adminUsers":[admin.id for admin in email.adminUsers.all()],
                        "memberUsers":[member.id for member in email.memberUsers.all()],
                        "adminUsersF":[admin.first_name for admin in email.adminUsers.all()],
                        "memberUsersF":[member.first_name for member in email.memberUsers.all()],
                    }
                    for email in emailsVar
                ]

                # Send the response back as JSON
                return JsonResponse({'emails': email_data}, status=200)
            
            elif data.get('sentNum') == 3:
                #userVar = TemporaryUser.objects.get(id=1)
                userVar = request.user
                emailsVar = TeamEmail.objects.filter(memberUsers=userVar)

                email_data = [
                    {
                        "id": email.id,
                        "subject": email.subject,
                        "content": email.content,
                        "fromUser": email.fromUser.email,
                        "fromUserId": email.fromUser.id,
                        "adminUsers":[admin.id for admin in email.adminUsers.all()],
                        "memberUsers":[member.id for member in email.memberUsers.all()],
                        "adminUsersF":[admin.first_name for admin in email.adminUsers.all()],
                        "memberUsersF":[member.first_name for member in email.memberUsers.all()],
                    }
                    for email in emailsVar
                ]

                # Send the response back as JSON
                return JsonResponse({'emails': email_data}, status=200)
            elif data.get('sentNum') == 4:
                #userVar = TemporaryUser.objects.get(id=1)
                userVar = request.user
                emailsVar = TeamEmail.objects.filter(adminUsers=userVar)
                emailsVarMe = TeamEmail.objects.filter(memberUsers=userVar)

                combined_emails = emailsVar.union(emailsVarMe)

                email_data = [
                    {
                        "id": email.id,
                        "subject": email.subject,
                        "content": email.content,
                        "fromUser": email.fromUser.email,
                        "fromUserId": email.fromUser.id,
                        "adminUsers":[admin.id for admin in email.adminUsers.all()],
                        "memberUsers":[member.id for member in email.memberUsers.all()],
                        "adminUsersF":[admin.first_name for admin in email.adminUsers.all()],
                        "memberUsersF":[member.first_name for member in email.memberUsers.all()],
                    }
                    for email in combined_emails
                ]

                # Send the response back as JSON
                return JsonResponse({'emails': email_data}, status=200)
            
            else:
                return JsonResponse({'emails': "none"}, status=200)

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    # If the request is not POST
    return JsonResponse({'emails': "not Post"}, status=400)

def team_email_sent_view(request,pk,ok):
    getEmail = TeamEmail.objects.get(id = ok)

    getFiles = TeamEmailFiles.objects.filter(emailId = getEmail)

    #userRep = TemporaryUser.objects.get(id = pk)
    userRep = User.objects.get(id = pk)


    if request.method == "POST":
        form = TeamReplyComposeForm(request.POST,request.FILES)

        if form.is_valid():
            message = form.cleaned_data['message']
            try:
                replyModel = TeamReply(
                    fromUser = userRep,
                    emailId = getEmail,
                    content = message
                )

                replyModel.save()


                uploaded_files = request.FILES.getlist('file')
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        email_file = TeamReplyFiles(
                            fromUser=userRep,
                            emailId = getEmail,
                            replyid=replyModel, 
                            file=uploaded_file
                        )
                        email_file.save()  
                else:
                    print("No files were uploaded.")

                return redirect(f"../../emailSentView/{pk}/{ok}")
            
            except ObjectDoesNotExist:
                print("Does not Exists")

    else:
        form = TeamReplyComposeForm()
    
    allRep = TeamReply.objects.filter(emailId = getEmail)
    allRepFiles = TeamReplyFiles.objects.filter(emailId = getEmail)
        
    return render(request,"teamemailSentView.html",{'form':form,'emailCont':getEmail,'filesCont':getFiles,'allRep':allRep,'allRepFiles':allRepFiles,'userRep':userRep})

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIRECTORY = os.path.join(BASE_DIR, "")

def team_download_file(request, filename):
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
