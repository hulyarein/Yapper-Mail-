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

