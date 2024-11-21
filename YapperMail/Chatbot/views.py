from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse,HttpResponse
from .models import ChatPropmt
from django.contrib.auth.models import User
from .chatbotapi import Chatb
import requests
import json
import os



# Create your views here.

def show_promt_Disp(request):
    userid = request.user

    return render(request,'chatmodel.html',{"userPk":userid})


def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  
            messageInp= data.get("message")

            
            promptChat = ChatPropmt(
                fromUser=request.user,
                prompt_text=messageInp,
                fromAi=False,
            )
            promptChat.save()

            print(aireply(messageInp))

            response = {
                'message': 'successfull'
            }
            return JsonResponse(response, status=200)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def aireply(message):

    url = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-32B-Instruct"

    headers = {
        "Authorization": f'Bearer {Chatb()}'
    }


    data = {
        "inputs": f"{message}",
        "parameters": {
            "max_new_tokens": 20 
        }
    }

    response = requests.post(url, headers=headers, json=data)

    # Print the response (generated text)
    return response.json()


