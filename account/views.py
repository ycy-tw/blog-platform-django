
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import (
    LogInForm,
    RegistrationForm,
)


def login_view(request):

    user = request.user
    if user.is_authenticated:
        return redirect('article:home')

    context = {}
    if request.POST:
        form = LogInForm(request.POST)

        if form.is_valid():

            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            login(request, user)

            return redirect('article:home')

    else:
        form = LogInForm()

    context['form'] = form
    return render(request, "account/login.html", context)


def logout_view(request):
    logout(request)
    previous_page = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_page)


def register_view(request):

    user = request.user
    if user.is_authenticated:
        username = user.username
        return redirect('article:author_profile', author=username)

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('article:home')
    else:
        form = RegistrationForm()

    context['form'] = form
    return render(request, 'account/register.html', context)
