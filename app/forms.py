from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    nome = forms.CharField(max_length=30, required=True)
    sobrenome = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)  

    class Meta:
        model = User
        fields = ('username', 'nome', 'sobrenome', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso. Por favor, escolha outro.")
        return email
