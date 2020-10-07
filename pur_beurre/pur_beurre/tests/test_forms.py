import datetime

from django.utils import timezone
from django.contrib.auth.models import User

from pytest import mark

from accounts.forms import SignUpForm

####################
#### SignUpForm  ###
####################


def test_signup_form_labels():
    form = SignUpForm()
    assert form.fields['first_name'].label == 'Prénom'
    assert form.fields['last_name'].label == 'Nom'
    assert form.fields['email'].label == 'Courriel'


def test_signup_form_help_texts():
    form = SignUpForm()
    assert form.fields['first_name'].help_text == 'Requis.'
    assert form.fields['last_name'].help_text == 'Optionel.'
    assert form.fields['email'].help_text == 'Requis. Entrez une adresse email valide.'


@mark.django_db
def test_signup_valid_data():
    form = SignUpForm(data={
                            'username': 'Pierre26',
                            'first_name': 'Pierre',
                            'last_name': '',
                            'email': 'pierre@gmail.com',
                            'password1': 'monsupermdp1234',
                            'password2': 'monsupermdp1234'
                            })
    assert form.is_valid() == True

@mark.django_db
def test_signup_wrong_email():
    form = SignUpForm(data={
                            'username': 'Pierre26',
                            'first_name': 'Pierre',
                            'last_name': '',
                            'email': 'pierregmail.com',
                            'password1': 'monsupermdp1234',
                            'password2': 'monsupermdp1234'
                            })
    assert form.is_valid() == False

@mark.django_db
def test_signup_email_already_recorded():
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    form = SignUpForm(data={
                            'username': 'Pierre26',
                            'first_name': 'Pierre',
                            'last_name': '',
                            'email': 'lennon@thebeatles.com',
                            'password1': 'monsupermdp1234',
                            'password2': 'monsupermdp1234'
                            })
    assert form.is_valid() == False
