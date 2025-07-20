from django.contrib import admin
from .models import Language, Story
from django import forms

class StoryAdminForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = '__all__'
        widgets = {
            'ink_json_content': forms.Textarea(attrs={'cols': 80, 'rows': 40}),
        }

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name', )

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    form = StoryAdminForm
    filter_horizontal = ('available_languages',)
    list_display = ('title', 'author')
    fields = ('title', 'author', 'available_languages', 'ink_json_content')
    search_fields = ('title', 'author')

