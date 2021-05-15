from re import match

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from user_profile.forms import UserForm
from user_profile.models import MainCycle


def index(request):
    user = User.objects.filter(id=request.user.id)
    if len(user) > 0:
        mainCycle = MainCycle.objects.filter(user=request.user)[0]
        return render(request, 'index.html', {'user': user[0], 'mainCycle': mainCycle})
    else:
        return render(request, 'login.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {'invalid': True})
    else:
        return render(request, 'login.html', {'invalid': False})


def user_logout(request):
    logout(request)
    return redirect('login')


def user_registration(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            if password_is_valid(request.POST['password']):
                user = form.save()
                mainCycle = MainCycle()
                mainCycle.user = user
                mainCycle.save()
                user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'registration.html', {'invalid': False, 'incorrectPassword': True, 'form': form})
        else:
            return render(request, 'registration.html', {'invalid': True, 'incorrectPassword': False, 'form': form})
    else:
        form = UserForm()
        return render(request, 'registration.html', {'invalid': False, 'incorrectPassword': False, 'form': form})


def password_is_valid(password):
    if len(password) >= 8 and bool(match(f'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])', password)):
        return True
    return False
