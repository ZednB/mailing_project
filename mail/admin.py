from django.contrib import admin
from mail.models import NewsLetter, Client, Message, Log


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('scheduled_time', 'frequency', 'status', 'is_sent',)

# @admin.site.register(Client)
# @admin.site.register(Message)
# @admin.site.register(Log)
