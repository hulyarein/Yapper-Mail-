from django.shortcuts import render,get_object_or_404,redirect
from .forms import EmailComposeForm,ReplyComposeForm,EditEmailForm,EditReplyForm
from .models import Email,EmailFiles,TemporaryUser,Reply,ReplyFiles
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.http import FileResponse, Http404
import os
from urllib.parse import unquote
import json
from django.http import JsonResponse,HttpResponse


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
    getEmail = Email.objects.get(id = 7)

    getFiles = EmailFiles.objects.filter(emailId = getEmail)

    userRep = TemporaryUser.objects.get(id = 3)


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

                return redirect("../emailSentView")
            
            except ObjectDoesNotExist:
                print("Does not Exists")

    else:
        form = ReplyComposeForm()
    
    allRep = Reply.objects.filter(emailId = getEmail)
    allRepFiles = ReplyFiles.objects.filter(emailId = getEmail)
        
    return render(request,"emailSentView.html",{'form':form,'emailCont':getEmail,'filesCont':getFiles,'allRep':allRep,'allRepFiles':allRepFiles})

def email_reply_view(request):

    if request.method == "POST":
        form = ReplyComposeForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data['message']

            try:
                emailRep = Email.objects.get(id = pk)
                userRep = TemporaryUser.objects.get(id = 3)

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

def edit_email(request,pk):
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

                return redirect(f'../emailSentView')
            except ObjectDoesNotExist:
                error_message = True
        else:
            print("not valid")




    else:
        initialValue = {
            'toUser':getEmail.toUser,
            'subject':getEmail.subject,
            'description':getEmail.content,
        }
        form = EditEmailForm(initial = initialValue)

    return render(request,"editEmail.html",{'form':form,'emailSent':getEmail,'emailFilesSent':getFiles})

def editExistingImage(request,pk):
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
            email_instance = get_object_or_404(Email, id=pk)

            # Query files linked to the email instance and filter by filenames
            files_to_delete = EmailFiles.objects.filter(emailId=email_instance).exclude(file__in=list_to_delete)
            deleted_files_count = files_to_delete.delete()

            response = {
                'message': 'Files deleted successfully',
                'deleted_files_count': deleted_files_count[0]  # Number of deleted files
            }
            return JsonResponse(response, status=200)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)




def edit_reply(request,pk):
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

                return redirect("../emailSentView")

            except ObjectDoesNotExist:
                print("Does Not exist")



    else:
        initialValue = {
            'description':getReply.content
        }
        form = EditReplyForm(initial=initialValue)

    return render(request,"editReply.html",{'form':form,'myfiles':getReplyFiles,'reply':getReply})

def existingReplyFile(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            list_to_delete = data.get('listme', [])  # Get list of filenames to delete
            print(list_to_delete)

            # Get the email instance by primary key (pk)
            reply_instance = get_object_or_404(Reply, id=pk)

            # Query files linked to the email instance and filter by filenames
            files_to_delete = ReplyFiles.objects.filter(replyid=reply_instance).exclude(file__in=list_to_delete)
            deleted_files_count = files_to_delete.delete()

            response = {
                'message': 'Files deleted successfully',
                'deleted_files_count': deleted_files_count[0]  # Number of deleted files
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

