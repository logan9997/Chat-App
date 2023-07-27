from django.shortcuts import redirect
from django.http import HttpRequest

def logout(request:HttpRequest):
    request.session['name'] = None
    return redirect('home')