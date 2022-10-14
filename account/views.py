from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserLoginForm, RegisterForm
from video.models import Video

# Create your views here.

def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("dashboard")
    return render(request, 'account/form.html', {"form": form, "title": title})

@login_required
def dashboard_view(request):
    videos = Video.objects.filter(uploader=request.user)
    return render(request, 'account/dashboard.html', {'videos':videos})

def register_view(request):
    title = "Register"
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("/")
    return render(request, 'account/form.html', {"form": form, "title": title})

def logout_view(request):
    logout(request)
    return render(request, 'video/home.html', {})
