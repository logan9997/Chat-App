from django.shortcuts import render, redirect
from ..models import Message
from django.http import HttpRequest
from ..config import MESSAGE_MAX_LENGTH

def home(request:HttpRequest):

    name = request.session.get('name')
    if name == None:
        return redirect('login')
    
    messages = Message.objects.all()

    context = {
        'name': name,
        'messages': messages,
        'MESSAGE_MAX_LENGTH': MESSAGE_MAX_LENGTH
    }
    return render(request, 'App/home.html', context)