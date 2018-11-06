from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import User_Creation_Form
from django.contrib.auth import authenticate, login, logout




def log_in(request):
    if request.method == "GET":
        form = AuthenticationForm()
        return render(request, 'authentication/login.html', {'form': form})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            next = request.GET.get('next')
            if next in ('/auth/register', '/auth/login'):
                return redirect('/nodeads/')
            elif next:
                return redirect(next)
        else:
            return render(request, "authentication/login_incorrect.html")


def log_out(request):
    logout(request)
    return redirect(request.GET.get('next'))

def register(request):
    if request.method == "GET":
        form = User_Creation_Form()
        return render(request, 'authentication/register.html', {'form': form})
    else:
        form = User_Creation_Form(request.POST)
        if form.is_valid():
            form.save()
        next = request.GET.get('next')
        if next in ('/auth/register', '/auth/login'):
            return redirect('/nodeads/')
        elif next:
            return redirect(next)
        else:
            return redirect('/nodeads/')