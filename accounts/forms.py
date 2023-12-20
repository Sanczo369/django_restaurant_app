from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Wprowadź Hasło',
        'class': 'form-controls'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Powtórz Hasło',
        'class': 'form-controls'
    }))

    
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email','password']
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']= 'Podaj Imię'
        self.fields['last_name'].widget.attrs['placeholder']= 'Podaj Nazwisko'
        self.fields['phone_number'].widget.attrs['placeholder']= 'Podaj Numer Telefonu'
        self.fields['email'].widget.attrs['placeholder']= 'Podaj Adres Email'
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'