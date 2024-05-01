
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login,  logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreationForm
# Create your views here.


def login_accounts(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':

        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(
                    request, messages.SUCCESS, 'LOG IN SUCCESS!!!')
                return redirect("/")
        else:
            messages.add_message(request, messages.ERROR,
                                 'incorect username or password')

    form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def signup_accounts(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'accounts/login.html')
    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


@login_required
def logout_accounts(request):

    logout(request)
    return redirect('/')
