from django.shortcuts import render, redirect

def home(request):

    name = request.session.get('name')
    if name == None:
        return redirect('login')

    context = {
        'name': name
    }
    return render(request, 'App/home.html', context)