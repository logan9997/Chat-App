from django.shortcuts import render, redirect
from ..models import Message
from django.http import HttpRequest
from ..config import MESSAGE_MAX_LENGTH

def home(request:HttpRequest):

    name = request.session.get('name')
    if name == None:
        return redirect('login')
    
    messages = Message.objects.all()

    #group message by date
    messages_by_date = {}
    for message in messages:
        date = str(message.date_sent).split(' ')[0]
        if date not in messages_by_date:
            messages_by_date[date] = []
        messages_by_date[date].append(message)

    messages = dict(sorted(messages_by_date.items()))
    
    context = {
        'name': name,
        'messages': messages,
        'MESSAGE_MAX_LENGTH': MESSAGE_MAX_LENGTH
    }
    return render(request, 'App/home.html', context)