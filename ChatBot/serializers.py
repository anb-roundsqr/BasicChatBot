from rest_framework import serializers
from ChatBot.models import BotQuestions


class ClientQuestionSerializer(serializers.ModelSerializer):

    class Meta:

        model = BotQuestions
        fields = '__all__'
