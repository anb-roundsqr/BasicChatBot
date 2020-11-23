from django.contrib import admin
from ChatBot.models import Conversation, BotConfiguration, CustomerBots
# Register your models here.

admin.site.register(Conversation)


class BotConfigurationAdmin(admin.ModelAdmin):
    def customer_name(self, obj):
        return obj.customer.name

    def bot_name(self, obj):
        return obj.bot.name

    list_display = ('question', 'customer_name', 'bot_name')
    search_fields = ('question',)


admin.site.register(BotConfiguration, BotConfigurationAdmin)


class CustomerBotAdmin(admin.ModelAdmin):
    def customer_name(self, obj):
        return obj.customer.name

    def bot_name(self, obj):
        return obj.bot.name

    list_display = ('source_url', 'customer_name', 'bot_name')
    search_fields = ('source_url',)


admin.site.register(CustomerBots, CustomerBotAdmin)
