from django.shortcuts import render, redirect
from ..forms import Login

def login(request):
    context = {
        'name_unfilled': False
    }

    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('name')
            request.session['name'] = username
            return redirect('home')
        else:
            context['name_unfilled'] = True

    return render(request, 'App/login.html', context=context)