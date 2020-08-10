from rest_framework import serializers
from ChatBot.models import ClientQuestions


class ClientQuestionSerializer(serializers.ModelSerializer):

    class Meta:

        model = ClientQuestions
        fields = '__all__'
