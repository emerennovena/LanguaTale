from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.welcome, name="welcome"),
    path('home/', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='welcome'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('account/', views.account, name='account'),
    path('story/<int:story_id>/play/<int:language_id>/', views.play_story, name='play_story'),
    path('api/tts/<int:story_id>/<int:language_id>/', views.generate_tts, name='generate_tts'),
    path('completed_stories/', views.completed_stories, name='completed_stories'),
    path('api/story_completed/<int:story_id>/<int:language_id>/', views.story_completed, name='story_completed'),
    path('api/completed_stories/', views.get_completed_stories_api, name='api_completed_stories'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view( template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)