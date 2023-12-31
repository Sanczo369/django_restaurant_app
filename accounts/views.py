from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth

from accounts.models import Account
from .forms import RegistrationForm


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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
            
            
            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = "Aktywuj konto"
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            from_email = 'test.test.test@vp.pl'
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email], from_email=from_email)
            send_email.send()          
            return redirect('/accounts/login/?command=verification&email='+email)
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


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Gratulacje! Twoje konto jest aktywne')
        return redirect('login')
    else:
        messages.error(request, "Nieprawidłowy link aktywujący")
    return redirect('register')

def resetpassword_validation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Proszę zresetuj swoje Hasło')
        return redirect('resetPassword')
    else:
        messages.error(request, "Nieprawidłowy link aktywujący")
        return redirect('register')