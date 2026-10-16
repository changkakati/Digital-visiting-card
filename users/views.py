from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('users:login_user')
        else:
            # If form is invalid, show errors
            return render(request, 'users/register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('cards:list_cards')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('users:login_user')
