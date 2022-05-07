from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class PostAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'notify_text', 'category', 'date', 'is_seen')
