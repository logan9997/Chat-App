from django.shortcuts import render, redirect
from ..forms import Login
from django.http import HttpRequest

def login(request:HttpRequest):
    context = {
        'name_unfilled': False
    }

    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            request.session['name'] = name
            return redirect('home')
        else:
            context['name_unfilled'] = True

    return render(request, 'App/login.html', context=context)