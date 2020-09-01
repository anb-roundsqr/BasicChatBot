from django.contrib import admin
from ChatBot.models import Conversation, BotConfiguration
# Register your models here.
admin.site.register(BotConfiguration)
admin.site.register(Conversation)
