from django.contrib import admin
from .models import Problems

# Register your models here.
class ProblemsAdmin(admin.ModelAdmin):
    list_display = ['title', 'time_limit', 'memory_limit', 'max_score']
    search_fields = ['title']

admin.site.register(Problems, ProblemsAdmin)