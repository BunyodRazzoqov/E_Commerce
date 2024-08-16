from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from my_web.forms import LoginForm, RegisterModelForm
from my_web.models import Customer


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email: str = form.cleaned_data['email']
            password: str = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('project_management')
            else:
                messages.error(request, 'Invalid Username or Password')
    else:
        form = LoginForm()
    return render(request, 'my_web/auth/login.html', {'form': form})


def register_page(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('customers')
    else:
        form = RegisterModelForm()
    context = {'form': form}
    return render(request, 'my_web/auth/register.html', context)


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('customers')
