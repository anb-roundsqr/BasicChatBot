from django.db import models
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _


class Customers(models.Model):

    objects = models.Manager

    CustomerID = models.TextField(null=True)
    name = models.CharField(max_length=200, null=False)
    org_name = models.CharField(max_length=100, unique=True)
    domain = models.SlugField(unique=True)
    email_id = models.EmailField(
        max_length=200, null=False, blank=False, unique=True)
    mobile = models.BigIntegerField(null=False, blank=False, unique=True)
    date_joined = models.DateTimeField(null=False, blank=False)
    date_modified = models.DateTimeField(null=True, blank=True)
    created_by_id = models.IntegerField()
    updated_by_id = models.IntegerField()
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    logo_path = models.TextField(default='static/images/default/org_logo.png')

    class Meta:
        app_label = 'ChatBot'


class Bots(models.Model):

    objects = models.Manager

    BotID = models.TextField(null=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    bot_type = models.TextField(null=True)
    domain = models.TextField(null=True)
    source_url = models.TextField(null=True)
    model_name = models.CharField(max_length=125, null=True)

    class Meta:
        app_label = 'ChatBot'


class Conversation(models.Model):

    objects = models.Manager

    # ConversationRecordID
    bot = models.ForeignKey(Bots, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    bot_origin_url = models.TextField()
    ip_address = models.TextField(null=True)
    session_id = models.TextField()
    event_name = models.TextField()  # bot or user response
    time_stamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    sender = models.CharField(max_length=10)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    browser = models.TextField(null=True)
    update_date_time = models.DateTimeField()

    class Meta:
        app_label = 'ChatBot'


class BotQuestions(models.Model):  # BotConfiguration

    objects = models.Manager

    id = models.AutoField(primary_key=True)
    bot = models.ForeignKey(Bots, on_delete=models.CASCADE)
    question = models.TextField(max_length=250)
    description = models.TextField(max_length=500, null=True)
    question_id = models.IntegerField()
    ANSWER_TYPE = Choices(
        ('TEXT', 'text', _('TEXT')),
        ('NUMBER', 'number', _('NUMBER')),
        ('RADIO', 'radio', _('RADIO')),
        ('DROPDOWN', 'dropdown', _('DROPDOWN')),
        ('CHECKBOX', 'checkbox', _('CHECKBOX')),
        ('FILE', 'file', _('FILE')),
        ('DATE', 'date', _('DATE')),
    )
    answer_type = models.CharField(max_length=10, choices=ANSWER_TYPE)
    suggested_answers = models.TextField(default=[])
    suggested_jump = models.TextField(default=[])
    validation1 = models.TextField(default="")
    validation2 = models.TextField(default="")
    error_msg = models.TextField(default="")
    # created_by_id = models.IntegerField()
    # updated_by_id = models.IntegerField()
    date_created = models.DateTimeField(null=False, blank=False)
    date_modified = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    required = models.CharField(max_length=4, default="no")
    related = models.BooleanField(default=False)

    class Meta:
        app_label = 'ChatBot'
        db_table = '%s_client_questions' % app_label
