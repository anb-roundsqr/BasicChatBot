from django.contrib import admin
from ChatBot.models import Conversation, BotQuestions
# Register your models here.
admin.site.register(BotQuestions)
admin.site.register(Conversation)
