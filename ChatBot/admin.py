from django.contrib import admin
from ChatBot.models import Conversation, BotConfiguration, CustomerBots
# Register your models here.
admin.site.register(BotConfiguration)
admin.site.register(Conversation)


class CustomerBotAdmin(admin.ModelAdmin):
    def customer_name(self, obj):
        return obj.customer.name

    def bot_name(self, obj):
        return obj.bot.name

    list_display = ('customer_name', 'bot_name', 'source_url')
    search_fields = ('source_url',)


admin.site.register(CustomerBots, CustomerBotAdmin)
