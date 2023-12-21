from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth

from accounts.models import Account
from .forms import RegistrationForm

# Create your views here.
def login(request):
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            
            auth.login(request, user)
            return redirect('home')
    
            
        else:
            messages.error(request, 'Nieprawidłowe dane logowania')
            return redirect('login')
    return render(request, 'accounts/login.html')


def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username=email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=username)
            user.phone_number = phone_number
            user.save()
            return redirect('register')
    else:  
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



def forgotPassword(request):
    return render(request, 'accounts/forgotPassword.html')