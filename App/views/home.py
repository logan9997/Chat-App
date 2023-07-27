from django.shortcuts import render, redirect
from ..models import Message
from django.http import HttpRequest

def home(request:HttpRequest):

    name = request.session.get('name')
    if name == None:
        return redirect('login')
    
    messages = Message.objects.all()


    context = {
        'name': name,
        'messages': messages,
        'max_msg_chars': 500
    }
    return render(request, 'App/home.html', context)