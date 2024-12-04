from django.shortcuts import render,get_object_or_404,redirect
from .forms import EmailComposeForm,ReplyComposeForm,EditEmailForm,EditReplyForm,SearchForm
from .models import Email,EmailFiles,TemporaryUser,Reply,ReplyFiles
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, Http404
import os
from urllib.parse import unquote
import json
from django.http import JsonResponse,HttpResponse
from django.db.models import Q


# Create your views here.

def email_composition(request,pk):
    error_message = False
    if request.method == "POST":
        form = EmailComposeForm(request.POST,request.FILES)
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
        form = EmailComposeForm()

    return render(request,"composeEmail.html",{'form':form,"errormessage":error_message})


def email_sent_view(request,pk,ok):
    getEmail = Email.objects.get(id = ok)

    getFiles = EmailFiles.objects.filter(emailId = getEmail)

    #userRep = TemporaryUser.objects.get(id = pk)
    userRep = User.objects.get(id = pk)


    if request.method == "POST":
        form = ReplyComposeForm(request.POST,request.FILES)

        if form.is_valid():
            message = form.cleaned_data['message']
            try:
                replyModel = Reply(
                    fromUser = userRep,
                    emailId = getEmail,
                    content = message
                )

                replyModel.save()


                uploaded_files = request.FILES.getlist('file')
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        email_file = ReplyFiles(
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
        form = ReplyComposeForm()
    
    allRep = Reply.objects.filter(emailId = getEmail)
    allRepFiles = ReplyFiles.objects.filter(emailId = getEmail)
        
    return render(request,"emailSentView.html",{'form':form,'emailCont':getEmail,'filesCont':getFiles,'allRep':allRep,'allRepFiles':allRepFiles,'userRep':userRep})

def email_reply_view(request):

    if request.method == "POST":
        form = ReplyComposeForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data['message']

            try:
                emailRep = Email.objects.get(id = pk)
                userRep = models.CustomUser.objects.get(id = 3)

                replyModel = Reply(
                    fromUser = userRep,
                    emailId = emailRep,
                    content = message
                )

                replyModel.save()

            
            except ObjectDoesNotExist:
                print("Does not Exists")



    else:
        form = ReplyComposeForm()

        
    return render(request,"emailReceiveView.html",{'form':form})

def edit_email(request,pk,uk):
    getEmail = Email.objects.get(id = pk)
    getFiles = EmailFiles.objects.filter(emailId = getEmail)
    
    if request.method == "POST":
        form = EditEmailForm(request.POST)
        if form.is_valid():
            toUser = form.cleaned_data['toUser']
            subject = form.cleaned_data['subject']
            description = form.cleaned_data['description']

            try:
                getEmail.subject = subject
                getEmail.content = description

                getEmail.save()

                uploaded_files = request.FILES.getlist('file')
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        email_file = EmailFiles(
                            fromUser=getEmail.fromUser,
                            toUser=getEmail.toUser,
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
            'toUser':getEmail.toUser.email,
            'subject':getEmail.subject,
            'description':getEmail.content,
        }
        form = EditEmailForm(initial = initialValue)

    return render(request,"editEmail.html",{'form':form,'emailSent':getEmail,'emailFilesSent':getFiles,"userRep":uk})

def editExistingImage(request,pk):
    '''getEmail = Email.objects.get(id = pk)
    getFiles = EmailFiles.objects.filter(emailId = getEmail)

    print(getFiles)
    return JsonResponse({"ok":"OK"})'''
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # 
            list_to_delete = data.get('listme', [])  # 
            print(list_to_delete)

            #
            email_instance = get_object_or_404(Email, id=pk)

            
            files_to_delete = EmailFiles.objects.filter(emailId=email_instance).exclude(file__in=list_to_delete)
            deleted_files_count = files_to_delete.delete()

            response = {
                'message': 'Files deleted successfully',
                'deleted_files_count': deleted_files_count[0]  # 
            }
            return JsonResponse(response, status=200)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)




def edit_reply(request,pk,uk):
    getReply = Reply.objects.get(id = pk)
    getReplyFiles = ReplyFiles.objects.filter(replyid = getReply)
    if request.method == "POST":
        form = EditReplyForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data["description"]

            try:
                getReply.content = description
                getReply.save()

                uploaded_files = request.FILES.getlist('file')
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        email_file = ReplyFiles(
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
        form = EditReplyForm(initial=initialValue)

    return render(request,"editReply.html",{'form':form,'myfiles':getReplyFiles,'reply':getReply,'userRep':uk})

def existingReplyFile(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  #
            list_to_delete = data.get('listme', [])  # 
            print(list_to_delete)

            # 
            reply_instance = get_object_or_404(Reply, id=pk)

            # 
            files_to_delete = ReplyFiles.objects.filter(replyid=reply_instance).exclude(file__in=list_to_delete)
            deleted_files_count = files_to_delete.delete()

            response = {
                'message': 'Files deleted successfully',
                'deleted_files_count': deleted_files_count[0]  # 
            }
            return JsonResponse(response, status=200)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



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
    


def emailListView(request):
    form = SearchForm()

    #userVar = TemporaryUser.objects.get(id = 1)
    userVar = request.user
    emailsVar = Email.objects.filter((Q(fromUser=userVar) | Q(toUser=userVar)) & Q(isDeleted = False))
    deletedEmails = Email.objects.filter((Q(fromUser=userVar) | Q(toUser=userVar)) & Q(isDeleted = False))
    return render(request,'emailList.html',{'form':form,'emails':emailsVar,'LogUser':userVar})

def sentEmailList(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            if data.get('sentNum') == 2:
                #userVar = TemporaryUser.objects.get(id=1)
                userVar = request.user
                emailsVar = Email.objects.filter(Q(fromUser=userVar) & Q(isDeleted = False))

                email_data = [
                    {
                        "id": email.id,
                        "subject": email.subject,
                        "content": email.content,
                        "fromUser": email.fromUser.email,
                        "toUser":email.toUser.email
                    }
                    for email in emailsVar
                ]

                # 
                return JsonResponse({'emails': email_data}, status=200)
            
            elif data.get('sentNum') == 3:
                #userVar = TemporaryUser.objects.get(id=1)
                userVar = request.user
                emailsVar = Email.objects.filter(Q(toUser=userVar) & Q(isDeleted = False))

                email_data = [
                    {
                        "id": email.id,
                        "subject": email.subject,
                        "content": email.content,
                        "fromUser": email.fromUser.email,
                        "toUser":email.toUser.email
                    }
                    for email in emailsVar
                ]

                # 
                return JsonResponse({'emails': email_data}, status=200)
            elif data.get('sentNum') == 4:
                #userVar = TemporaryUser.objects.get(id=1)
                userVar = request.user
                emailsVar = Email.objects.filter((Q(fromUser=userVar) | Q(toUser=userVar)) & Q(isDeleted = False))

                email_data = [
                    {
                        "id": email.id,
                        "subject": email.subject,
                        "content": email.content,
                        "fromUser": email.fromUser.email,
                        "toUser":email.toUser.email
                    }
                    for email in emailsVar
                ]

                return JsonResponse({'emails': email_data}, status=200)
            
            elif data.get('sentNum') == 5:
                #userVar = TemporaryUser.objects.get(id=1)
                userVar = request.user
                emailsVar = Email.objects.filter(Q(isDeleted = True))

                email_data = [
                    {
                        "id": email.id,
                        "subject": email.subject,
                        "content": email.content,
                        "fromUser": email.fromUser.email,
                        "toUser":email.toUser.email
                    }
                    for email in emailsVar
                ]
                
                return JsonResponse({'emails': email_data}, status=200)
            
            else:
                return JsonResponse({'emails': "none"}, status=200)

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    #
    return JsonResponse({'emails': "not Post"}, status=400)


def deleteEmailFunc(request):
    try:
        data = json.loads(request.body)
        email_id = data.get('delId')

        if not email_id:
            return JsonResponse({'message': 'Email ID is required.'}, status=400)

        emailsVar = Email.objects.get(id=email_id)

        if emailsVar.isDeleted:
            emailsVar.isDeleted = False
            emailsVar.save()

            return JsonResponse({'message': 'Email recovered successfully.'}, status=200)
        else:
            emailsVar.isDeleted = True
            emailsVar.save()

            return JsonResponse({'message': 'Email deleted successfully.'}, status=200)

    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Email not found.'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

    except Exception as e:
        # 
        print(f"Unexpected error: {e}")
        return JsonResponse({'message': 'An error occurred while deleting the email.'}, status=500)



def deleteReplyFunc(request):
    try:
        data = json.loads(request.body)
        reply_id = data.get('delId')

        if not reply_id:
            return JsonResponse({'message': 'Reply ID is required.'}, status=400)

        # 
        replyVar = Reply.objects.get(id=reply_id)
        replyVar.delete()

        return JsonResponse({'message': 'Reply deleted successfully.'}, status=200)

    except ObjectDoesNotExist:
        return JsonResponse({'message': 'Reply not found.'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON data.'}, status=400)

    except Exception as e:
        # 
        print(f"Unexpected error: {e}")
        return JsonResponse({'message': 'An error occurred while deleting the reply.'}, status=500)