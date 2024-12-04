from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse,HttpResponse
from .models import ChatPropmt
from django.contrib.auth.models import User
from .chatbotapi import Chatb
import requests
import json
import os
from django.templatetags.static import static
from huggingface_hub import InferenceClient



# Create your views here.

def show_promt_Disp(request):
    userid = request.user
    userPrompt = ChatPropmt.objects.filter(fromUser = userid)


    profilepic = userid.profile_picture.url if userid.profile_picture else static('images/default_profile.jpg')

    return render(request,'chatmodel.html',{"userPk":userid,"profilepic":profilepic,"userPrompt":userPrompt})


def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  
            messageInp= data.get("message")

        

            contentAi = aireply(messageInp)

            promptChat = ChatPropmt(
                fromUser=request.user,
                prompt_text=messageInp,
                fromAi=False,
            )
            promptChat.save()

            aiChat = ChatPropmt(
                fromUser=request.user,
                prompt_text=contentAi,
                fromAi=True,
            )
            aiChat.save()

            response = {
                'message': contentAi,
                "yourId":promptChat.id
            }
            return JsonResponse(response, status=200)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)
        except Exception:
            return JsonResponse({'error': 'an error occured'}, status=405)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def aireply(message):
    print("good")

    client = InferenceClient(api_key=Chatb())

    messages = [
	    {
		    "role": "user",
		    "content": message
	    }
    ]

    completion = client.chat.completions.create(
        model="Qwen/QwQ-32B-Preview", 
	    messages=messages, 
	    max_tokens=500
    )

    return completion.choices[0].message.content

def delete_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  
            idInp= data.get("idInp")

            delprompt = get_object_or_404(ChatPropmt,id = idInp)
            delprompt.delete()

            return JsonResponse({"message":"Success"},status = 200)
        except Exception:
            return JsonResponse({"error":"An error occured"},status = 405)
    else:
        return JsonResponse({"error":"Not a json"},status = 405)
    
def clear_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            idDel = data.get("idDel")

            delallprompt = ChatPropmt.objects.filter(fromUser = idDel)
            if delallprompt.exists():
                delallprompt.delete()

            return JsonResponse({"message":"Success"},status = 200)
        except Exception:
            return JsonResponse({"error":"An error Occured"},status = 405)
    else:
        return JsonResponse({"error":"Not a Post"},status = 405)



