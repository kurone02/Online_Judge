from django.contrib import admin
from .models import Problems
from .models import Submission

# Register your models here.
class ProblemsAdmin(admin.ModelAdmin):
    list_display = ['title', 'time_limit', 'memory_limit', 'max_score']
    search_fields = ['title']

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'user', 'problem', 'language', 'verdict']
    list_filter = ['user', 'problem', 'verdict']
    search_fields = ['id']

admin.site.register(Problems, ProblemsAdmin)
admin.site.register(Submission, SubmissionAdmin)