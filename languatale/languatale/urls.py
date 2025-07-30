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
    path('api/ink_json/<int:story_id>/<int:language_id>/', views.get_ink_json, name='get_ink_json'),
    path('api/tts/<int:story_id>/<int:language_id>/', views.generate_tts, name='generate_tts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)