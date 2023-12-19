from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth

# Create your views here.
def login(request):
    return render(request, 'accounts/login.html')


def register(request):
    return render(request, 'accounts/register.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Zostałeś wylogowany.')
    return render(request, 'accounts/login.html')
