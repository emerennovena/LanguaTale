from django.shortcuts import render, redirect
from .models import Story, Language

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