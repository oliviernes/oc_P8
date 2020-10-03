from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='Prénom', max_length=30, required=True, help_text='Requis.')
    last_name = forms.CharField(label='Nom', max_length=30, required=False, help_text='Optionel.')
    email = forms.EmailField(label='Courriel', max_length=254, help_text='Requis. Entrez une adresse email valide.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
