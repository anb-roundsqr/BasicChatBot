from rest_framework import serializers
from ChatBot.models import BotConfiguration, Customers, Bots, CustomerBots, BulkQuestion


class ClientQuestionSerializer(serializers.ModelSerializer):

    class Meta:

        model = BotConfiguration
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:

        model = Customers
        fields = ['url', 'id', 'name', 'org_name']


class CustomerListSerializer(serializers.ModelSerializer):

    class Meta:

        model = Customers
        fields = ['url', 'id', 'name', 'org_name', 'logo_path']


class CustomerRetrieveSerializer(serializers.ModelSerializer):

    class Meta:

        model = Customers
        fields = '__all__'


class CustomerCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Customers
        fields = [
            'url', 'id', 'name', 'web_url',
            'org_name', 'email_id', 'mobile',
            'date_joined', 'created_by_id'
        ]


class CustomerUpdateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Customers
        fields = [
            'url', 'id', 'name', 'web_url', 'email_id', 'mobile',
            'org_name', 'date_modified', 'updated_by_id'
        ]


class CustomerDeleteSerializer(serializers.ModelSerializer):

    class Meta:

        model = Customers
        fields = ['url', 'id', 'date_modified', 'updated_by_id', 'is_deleted']


class BotSerializer(serializers.ModelSerializer):

    class Meta:

        model = Bots
        fields = ['url', 'id', 'name', 'description', 'model_name']


class BotCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Bots
        fields = [
            'url', 'id', 'name', 'description',
            'model_name', 'date_created', 'created_by_id'
        ]


class BotListSerializer(serializers.ModelSerializer):

    class Meta:

        model = Bots
        fields = ['url', 'id', 'name']


class BotRetrieveSerializer(serializers.ModelSerializer):

    class Meta:

        model = Bots
        fields = '__all__'


class BotUpdateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Bots
        fields = [
            'url', 'id', 'name', 'description',
            'model_name', 'date_modified', 'updated_by_id'
        ]


class CustomerBotSerializer(serializers.ModelSerializer):

    class Meta:

        model = CustomerBots
        fields = [
            'url', 'id', 'customer', 'bot', 'source_url', 'bot_type',
            'header_colour', 'body_colour', 'font_type', 'bot_logo',
            'chat_logo', 'user_logo', 'bot_bubble_colour',
            'user_bubble_colour', 'chat_bot_font_colour',
            'chat_user_font_colour',
        ]


class CustomerBotListSerializer(serializers.ModelSerializer):

    class Meta:

        model = CustomerBots
        fields = [
            'url', 'id', 'source_url', 'bot_type', 'customer_id_text'
        ]


class CustomerBotRetrieveSerializer(serializers.ModelSerializer):

    class Meta:

        model = CustomerBots
        fields = '__all__'


class CustomerBotCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = CustomerBots
        fields = [
            'url', 'id', 'customer', 'bot', 'source_url', 'bot_type',
            'header_colour', 'body_colour', 'font_type', 'bot_logo',
            'chat_logo', 'user_logo', 'bot_bubble_colour',
            'user_bubble_colour', 'chat_bot_font_colour',
            'chat_user_font_colour', 'date_created',
            'created_by_id', 'customer_id_text', 'bot_id_text'
        ]


class CustomerBotUpdateSerializer(serializers.ModelSerializer):

    class Meta:

        model = CustomerBots
        fields = [
            'url', 'id', 'source_url', 'bot_type',
            'header_colour', 'body_colour', 'font_type', 'bot_logo',
            'chat_logo', 'user_logo', 'bot_bubble_colour',
            'user_bubble_colour', 'chat_bot_font_colour',
            'chat_user_font_colour', 'date_modified',
            'updated_by_id',
        ]


class QuestionListSerializer(serializers.ModelSerializer):

    class Meta:

        model = BotConfiguration
        exclude = ['description']
        order_by = ['-id']


class BulkQuestionSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = BulkQuestion
        fields = ('id', 'mapping_id', 'questions')
