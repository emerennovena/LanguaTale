# Filename: views.py
# Author: Emerentia Novena
# Date: 2025-08-07
# AI Usage Declaration:
# - This file contains code generated with the help of AI tools.
# - Tools used: ChatGPT
# - Date Generated: 2025-07-20
# - AI Generated Sections are marked with comments: // [AI-GENERATED]
# - I have reviewed, tested, and understood all AI-generated code.

# Note:
# - Any additional changes made since the original version are student-written.

import io

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from gtts import gTTS

from .forms import CustomSignUpForm
from .models import Story, Language, CompletedStory

# [STUDENT-WRITTEN]
def welcome(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'welcome.html')

# [STUDENT-WRITTEN]
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    stories = Story.objects.all().prefetch_related('available_languages')
    context = {
        'stories': stories,
        'username': request.user.username,
    }
    return render(request, 'home.html', context)

# [STUDENT-WRITTEN]
def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = CustomSignUpForm()
        return render(request, 'signup.html', {'form': form})

# [STUDENT-WRITTEN]
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def account(request):
    user = request.user
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'username': user.username,
    }
    return render(request, 'account.html', context)

# [AI-GENERATED: ChatGPT: 2025-07-20] - I was stuck in implementing a view that can fetch and render dynamic JSON content, and I was unable to find examples of how to securely pass the story data to the front-end template.
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def play_story(request, story_id, language_id):
    story = get_object_or_404(Story, pk=story_id)
    language = get_object_or_404(Language, pk=language_id)

    ink_json = None
    error_message = None

    if story.ink_json_content:
        language_id_str = str(language.id)
        ink_json = story.ink_json_content.get(language_id_str)

        if not ink_json:
            error_message = f"Ink story content not available for {language.name} (ID: {language.id})"
    else:
        error_message = "No Ink JSON content found for this story."

    context = {
        'story': story,
        'language': language,
        'ink_json_content': ink_json,
        'error_message': error_message,
    }
    return render(request, 'play_story.html', context)

# [AI-GENERATED: ChatGPT: 2025-07-20] - I was stuck in implementing TTS, and I was unable to find suitable examples or solutions for generating TTS from the python library (although there is the documentation) using Google.
@csrf_exempt
def generate_tts(request, story_id, language_id):
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if not text:
            return JsonResponse({'error': 'No text provided'}, status=400)
        map_language = {
            1: 'en',
            2: 'id',
            4: 'es',
        }
        lang_code = map_language.get(language_id, 'en')

        try:
            tts = gTTS(text=text, lang=lang_code)
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            return HttpResponse(mp3_fp.read(), content_type='audio/mpeg')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error':'Invalid method'}, status=405)

# [STUDENT-WRITTEN]
@login_required
def completed_stories(request):
    completed = CompletedStory.objects.filter(user=request.user)
    context = {
        'completed_stories': completed,
        'first_name': request.user.first_name,
    }
    return render(request, 'completed_stories.html', context)

# [STUDENT-WRITTEN]
@login_required
@require_POST
def story_completed(request, story_id, language_id):
    user = request.user
    try:
        story = Story.objects.get(id=story_id)
        language = Language.objects.get(id=language_id)
    except (Story.DoesNotExist, Language.DoesNotExist):
        return JsonResponse({'error': 'Story or language not found'}, status=404)

    completed_story, created = CompletedStory.objects.get_or_create(user=user, story=story, language=language)

    return JsonResponse({'success': True, 'completed': True})

# [STUDENT-WRITTEN]
@login_required
def get_completed_stories_api(request):
    completed_stories = CompletedStory.objects.filter(user=request.user).select_related('story', 'language')
    data = [
        {
            'story_id': cs.story.id,
            'story_title': cs.story.title,
            'language_id': cs.language.id if cs.language else None,
            'language_name': cs.language.name if cs.language else None,
        }
        for cs in completed_stories
    ]
    return JsonResponse({'completed_stories': data})