from EmailCompositionAndManagement.forms import EmailComposeForm
from EmailCompositionAndManagement.models import Email, EmailFiles, CategoryEmail
from landing.models import CustomUser
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from landing.models import CustomUser
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Create your views here.
from .models import Notification

@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    data = [{
        'id': notif.id,
        'title': notif.title,
        'message': notif.message,
        'from_user': notif.from_user,
        'is_read': notif.is_read
    } for notif in notifications]
    return JsonResponse({'notifications': data})

@login_required
def mark_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'failed', 'error': 'Notification not found'}, status=404)

def index(request, pk):
    error_message = False
    if request.method == "POST":
        

        form = EmailComposeForm(request.POST,request.FILES)
        if form.is_valid():
            toUser = form.cleaned_data['toUser']
            subject = form.cleaned_data['subject']
            description = form.cleaned_data['description']

            print("Email bruh", toUser)

            async_to_sync(get_channel_layer().group_send)(
                "global_notif",
                {
                    'type': 'receive',
                    'email': {
                        'fromUser': request.user.id, 
                        'toUser': toUser, 
                        'subject': subject,
                        'content': description
                    }
                }
            )


            try:
                fromUser = request.user
                toUserDatabase = CustomUser.objects.get(email = toUser)
                email = Email.objects.get_or_create(
                    fromUser=fromUser,
                    toUser=toUserDatabase,
                    subject=subject,
                    content=description
                )

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

                categemailFrom = CategoryEmail(
                    userCat = fromUser,
                    emaildCat = email[0]
                )
                categemailFrom.save()

                if fromUser != toUserDatabase:

                    categemailTo = CategoryEmail(
                        userCat = toUserDatabase,
                        emaildCat = email[0]
                    )
                    categemailTo.save()
                
                Notification.objects.create(
                    from_user = fromUser,
                    to_user = CustomUser.objects.filter(username=toUser).first(),
                    title = subject,
                    message = description,
                    email_id = email[0]
                )

                return redirect('emailListView')
            except CustomUser.DoesNotExist:
                error_message = True
            except IntegrityError as e:
                error_message = True
                messages.error(request, f"Database error: {e}")
            except Exception as e:
                error_message = True
                print(f"Unexpected error: {e}")
                messages.error(request, "An unexpected error occurred. Please try again.")
        else:
            print("Not working")
            print(form.errors)

    else:
        form = EmailComposeForm()

    return render(request,"index.html",{'form':form,"errormessage":error_message})
    # return render(request, 'index.html')


@csrf_exempt 
@login_required
def get_user_id(request):
    """
    Handles POST and GET requests:
    - POST: Process the provided email to find its associated user ID.
    - GET: Return both the processed email_user_id and the logged-in user ID.
    """
    global processed_email_user_id

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            if email:
                try:
                    user = CustomUser.objects.get(email=email)
                    processed_email_user_id = user.id
                    return JsonResponse({"message": "Email processed successfully"}, status=200)
                except CustomUser.DoesNotExist:
                    processed_email_user_id = None
                    return JsonResponse({"error": "User not found for provided email"}, status=404)
            return JsonResponse({"error": "Email not provided"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    elif request.method == "GET":
        logged_in_user_id = request.user.id if request.user.is_authenticated else None
        return JsonResponse({
            "logged_in_user_id": logged_in_user_id,
            "email_user_id": processed_email_user_id
        }, status=200)

    return JsonResponse({"error": "Unsupported method"}, status=405)


@login_required
def get_logged_in(request):
    logged_in = request.user.id if request.user.is_authenticated else None
    return JsonResponse({
            "logged_in": logged_in})


# views.py
@login_required
def notification_detail(request, email_id):
    print("GOT HERE LNAO AJDNASJNDSJAD")
    email = get_object_or_404(Email, id=email_id)
    print("Email", email)
    return render(request, 'notification_detail.html', {'email': email})
