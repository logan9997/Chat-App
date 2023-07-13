from django.shortcuts import redirect

def logout(request):
    request.session['name'] = None
    return redirect('home')