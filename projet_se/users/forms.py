# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import User

# class UserRegistrationForm(UserCreationForm):
#     first_name = forms.CharField(max_length=100)
#     last_name = forms.CharField(max_length=100)
#     email = forms.EmailField()
#     status = forms.ChoiceField(choices=User.STATUS_CHOICES)

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'status', 'password1', 'password2']
# forms.py
# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django.contrib.auth import authenticate

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    status = forms.ChoiceField(choices=User.STATUS_CHOICES)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'status', 'password1', 'password2']

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'autofocus': True}))

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Adresse email ou mot de passe incorrect.")
        return self.cleaned_data
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))


  

# class UpdateClientForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email']  # Ajoutez d'autres champs si nécessaire
#         widgets = {
#             'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
#         }

        

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UpdateClientForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # Ajoutez d'autres champs si nécessaire

