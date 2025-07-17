from django.contrib import admin
from .models import Language, Story

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', )

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    filter_horizontal = ('available_languages',)
    list_display = ('title', 'author')
    fields = ('title', 'author', 'available_languages', 'ink_json_content')
    search_fields = ('title', 'author')

