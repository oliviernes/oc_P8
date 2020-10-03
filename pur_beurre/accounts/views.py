from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect

from accounts.forms import SignUpForm, EmailLoginForm
# Create your views here.


def my_account(request):
    return render(request, "registration/account.html")


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ~ username = form.cleaned_data.get('username')
            # ~ raw_password = form.cleaned_data.get('password1')
            # ~ user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("my_account")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = EmailLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("my_account")
    else:
        form = EmailLoginForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return render(request, "registration/logged_out.html")
