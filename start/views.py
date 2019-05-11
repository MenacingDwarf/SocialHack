from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.contrib.auth.models import User


def home(request):
    if '_auth_user_id' not in request.session.keys():
        return redirect('/log')

    if 'st' in User.objects.get(id=request.session['_auth_user_id']).username:
        print('yes')
    else:
        print('no')

    return render(request, 'start/home.html')


def log(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['user'], password=request.POST['pass'])
        if user and user.is_active == True:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'start/log.html', {'message': 'Неверный логин или пароль'})

    return render(request, 'start/log.html')
