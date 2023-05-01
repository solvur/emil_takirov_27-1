from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from users.forms import RegisterForm, LoginForm


def register_view(request):
    if request.method == 'GET':
        context = {
            'form': RegisterForm
        }

        return render(request, 'users/register.html', context=context)

    if request.method == 'POST':
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            if form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
                User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password')
                )
                return redirect('/posts/')
            else:
                form.add_error('password1', 'password1 != password2')

        return render(request, 'users/register.html', context={
            'form': form
        })


def auth_view(request):
    if request.method == 'GET':
        context = {
            'form': LoginForm
        }

        return render(request, 'users/login.html', context=context)

    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = authenticate(request,
                                username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password')
                                )
            if user:
                login(request, user)
                return redirect('/products/')
            else:
                form.add_error('username', 'Authentication error')

        return render(request, 'users/login.html', context={
            'form': form
        })


def logout_view(request):
    logout(request)
    return redirect('/products')
