from django.contrib import admin

from .models import *

class PostModelAdmin(admin.ModelAdmin):
    # список полей которые мы хотим видеть в админ-панели:
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    # кликабельные поля:
    list_display_links = ('id', 'title')
    # по каким полям можно производить поиск информации:
    search_fields = ('title', 'content')
    # возможность редактирования:
    list_editable = ('is_published',)
    # добавление панели фильтрации
    list_filter = ('cat', 'time_create', 'is_published')
    prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class ContactAdminAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    list_display_links = ('name',)
    search_fields = ('name',)

admin.site.register(PostModel, PostModelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ContactAdmin, ContactAdminAdmin)