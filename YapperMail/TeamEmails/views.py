from django.shortcuts import render,get_object_or_404,redirect
from .forms import TeamEmailComposeForm,TeamReplyComposeForm,TeamEditEmailForm,TeamEditReplyForm,TeamSearchForm
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
    emailsVar = TeamEmail.objects.filter(Q(adminUsers=userVar) & Q(isDeleted = False))
    emailsVarMe = TeamEmail.objects.filter(Q(memberUsers=userVar) & Q(isDeleted = False))

    combined_emails = emailsVar.union(emailsVarMe)
    return render(request,'TeamemailList.html',{'form':form,'emails':combined_emails,'LogUser':userVar})

def team_sentEmailList(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            if data.get('sentNum') == 2:
                #userVar = TemporaryUser.objects.get(id=1)
                userVar = request.user
                emailsVar = TeamEmail.objects.filter(Q(adminUsers=userVar) & Q(isDeleted = False))

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
                emailsVar = TeamEmail.objects.filter(Q(memberUsers=userVar) & Q(isDeleted = False))

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
                emailsVar = TeamEmail.objects.filter(Q(adminUsers=userVar) & Q(isDeleted = False))
                emailsVarMe = TeamEmail.objects.filter(Q(memberUsers=userVar) & Q(isDeleted = False))

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
    


def team_edit_email(request,pk,uk):
    getEmail = TeamEmail.objects.get(id = pk)
    getFiles = TeamEmailFiles.objects.filter(emailId = getEmail)
    
    if request.method == "POST":
        form = TeamEditEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            description = form.cleaned_data['description']

            try:
                getEmail.subject = subject
                getEmail.content = description

                getEmail.save()

                uploaded_files = request.FILES.getlist('file')
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        email_file = TeamEmailFiles(
                            emailId=getEmail, 
                            file=uploaded_file
                        )
                        email_file.save()  
                else:
                    print("No files were uploaded.")

                return redirect(f'../../emailSentView/{uk}/{pk}')
            except ObjectDoesNotExist:
                error_message = True
        else:
            print("not valid")




    else:
        initialValue = {
            'subject':getEmail.subject,
            'description':getEmail.content,
        }
        form = TeamEditEmailForm(initial = initialValue)

    return render(request,"teameditEmail.html",{'form':form,'emailSent':getEmail,'emailFilesSent':getFiles,"userRep":uk})

def team_editExistingImage(request,pk):
    '''getEmail = Email.objects.get(id = pk)
    getFiles = EmailFiles.objects.filter(emailId = getEmail)

    print(getFiles)
    return JsonResponse({"ok":"OK"})'''
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            list_to_delete = data.get('listme', [])  # Get list of filenames to delete
            print(list_to_delete)

            # Get the email instance by primary key (pk)
            email_instance = get_object_or_404(TeamEmail, id=pk)

            # Query files linked to the email instance and filter by filenames
            files_to_delete = TeamEmailFiles.objects.filter(emailId=email_instance).exclude(file__in=list_to_delete)
            deleted_files_count = files_to_delete.delete()

            response = {
                'message': 'Files deleted successfully',
                'deleted_files_count': deleted_files_count[0]  # Number of deleted files
            }
            return JsonResponse(response, status=200)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def team_edit_reply(request,pk,uk):
    getReply = TeamReply.objects.get(id = pk)
    getReplyFiles = TeamReplyFiles.objects.filter(replyid = getReply)
    if request.method == "POST":
        form = TeamEditReplyForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data["description"]

            try:
                getReply.content = description
                getReply.save()

                uploaded_files = request.FILES.getlist('file')
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        email_file = TeamReplyFiles(
                            fromUser=getReply.fromUser,
                            emailId = getReply.emailId,
                            replyid= getReply, 
                            file=uploaded_file
                        )
                        email_file.save()  
                else:
                    print("No files were uploaded.")

                return redirect(f"../../emailSentView/{uk}/{getReply.emailId.id}")

            except ObjectDoesNotExist:
                print("Does Not exist")



    else:
        initialValue = {
            'description':getReply.content
        }
        form = TeamEditReplyForm(initial=initialValue)

    return render(request,"teameditReply.html",{'form':form,'myfiles':getReplyFiles,'reply':getReply,'userRep':uk})

def team_existingReplyFile(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            list_to_delete = data.get('listme', [])  # Get list of filenames to delete
            print(list_to_delete)

            # Get the email instance by primary key (pk)
            reply_instance = get_object_or_404(TeamReply, id=pk)

            # Query files linked to the email instance and filter by filenames
            files_to_delete = TeamReplyFiles.objects.filter(replyid=reply_instance).exclude(file__in=list_to_delete)
            deleted_files_count = files_to_delete.delete()

            response = {
                'message': 'Files deleted successfully',
                'deleted_files_count': deleted_files_count[0]  # Number of deleted files
            }
            return JsonResponse(response, status=200)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def teams_deleteReplyFunc(request):
    try:
        data = json.loads(request.body)
        reply_id = data.get('delId')

        if not reply_id:
            return JsonResponse({'message': 'Reply ID is required.'}, status=400)

        # Attempt to get the email by ID
        replyVar = TeamReply.objects.get(id=reply_id)
        replyVar.delete()

        return JsonResponse({'message': 'Reply deleted successfully.'}, status=200)

    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Reply not found.'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

    except Exception as e:
        # Log unexpected errors and return a generic error message
        print(f"Unexpected error: {e}")
        return JsonResponse({'message': 'An error occurred while deleting the reply.'}, status=500)
    

def team_deleteEmailFunc(request):
    try:
        data = json.loads(request.body)
        email_id = data.get('delId')

        if not email_id:
            return JsonResponse({'message': 'Email ID is required.'}, status=400)

        # Attempt to get the email by ID
        emailsVar = TeamEmail.objects.get(id=email_id)
        emailsVar.isDeleted = True
        emailsVar.save()

        return JsonResponse({'message': 'Email deleted successfully.'}, status=200)

    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Email not found.'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

    except Exception as e:
        # Log unexpected errors and return a generic error message
        print(f"Unexpected error: {e}")
        return JsonResponse({'message': 'An error occurred while deleting the email.'}, status=500)
    


def team_removeAccessMember(request,pk):
    try:
        data = json.loads(request.body)
        user_id = data.get('delId')

        if not user_id:
            return JsonResponse({'message': 'User ID is required.'}, status=400)

        # Attempt to get the email by ID
        teamVar = TeamEmail.objects.get(id=pk)
        teamVar.memberUsers.remove(user_id)

        return JsonResponse({'message': 'User deleted successfully.'}, status=200)

    except ObjectDoesNotExist:
        return JsonResponse({'message': 'User not found.'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

    except Exception as e:
        # Log unexpected errors and return a generic error message
        print(f"Unexpected error: {e}")
        return JsonResponse({'message': 'An error occurred while deleting the User.'}, status=500)
    
def team_removeAccessAdmin(request,pk):
    try:
        data = json.loads(request.body)
        user_id = data.get('delId')

        if not user_id:
            return JsonResponse({'message': 'User ID is required.'}, status=400)

        # Attempt to get the email by ID
        teamVar = TeamEmail.objects.get(id=pk)
        teamVar.adminUsers.remove(user_id)

        return JsonResponse({'message': 'User deleted successfully.'}, status=200)

    except ObjectDoesNotExist:
        return JsonResponse({'message': 'User not found.'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

    except Exception as e:
        # Log unexpected errors and return a generic error message
        print(f"Unexpected error: {e}")
        return JsonResponse({'message': 'An error occurred while deleting the User.'}, status=500)
    


def team_addAdmin(request,pk):
    try:
        data = json.loads(request.body)
        user_id = data.get('addId')

        if not user_id:
            return JsonResponse({'message': 'User ID is required.'}, status=400)

        # Attempt to get the email by ID
        userHold = User.objects.get(id = user_id)
        teamVar = TeamEmail.objects.get(id=pk)
        teamVar.adminUsers.add(userHold)
        teamVar.memberUsers.remove(userHold)

        return JsonResponse({'message': 'User added successfully.'}, status=200)

    except ObjectDoesNotExist:
        return JsonResponse({'message': 'User not found.'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

    except Exception as e:
        # Log unexpected errors and return a generic error message
        print(f"Unexpected error: {e}")
        return JsonResponse({'message': 'An error occurred while adding the User.'}, status=500)
    



