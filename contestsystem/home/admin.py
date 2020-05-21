from django.contrib import admin
from .models import Announcement

# Register your models here.
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']
    list_filter = ['date']
    search_fields = ['title']

admin.site.register(Announcement, AnnouncementAdmin)