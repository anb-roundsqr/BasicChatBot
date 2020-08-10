from django.db import models
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _


class Customers(models.Model):

    objects = models.Manager

    name = models.CharField(max_length=255)

    class Meta:
        app_label = 'ChatBot'


class Bots(models.Model):

    objects = models.Manager

    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)

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
    event_name = models.TextField()
    time_stamp = models.DateTimeField()
    text = models.TextField()
    chat_source_latitude = models.TextField()
    chat_source_longitude = models.TextField()
    browser = models.TextField()
    update_date_time = models.DateTimeField()

    class Meta:
        app_label = 'ChatBot'


class BotQuestions(models.Model):

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

    class Meta:
        app_label = 'ChatBot'
        db_table = '%s_client_questions' % app_label
