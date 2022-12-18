from django.contrib import admin
from .models import Post, Studio, Category, Genre

# Register your models here.

admin.site.register(Post)

class StudioAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(Studio, StudioAdmin)

class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class GenreAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name',)}

admin.site.register(Genre, GenreAdmin)