from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from .forms import RegistrationForm

# Create your views here.
def login(request):
    return render(request, 'accounts/login.html')


def register(request):
    form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html',context)

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Zostałeś wylogowany.')
    return render(request, 'accounts/login.html')
