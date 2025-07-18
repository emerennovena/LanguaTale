from django.shortcuts import render, redirect
from .models import Story, Language
from django.contrib.auth import login
from .forms import CustomSignUpForm

def welcome(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'welcome.html')

def home(request):
    stories = Story.objects.all().prefetch_related('available_languages')
    context = {
        'stories': stories,
        'username': request.user.username,
    }
    return render(request, 'home.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomSignUpForm()
    return render(request, 'signup.html', {'form': form})
