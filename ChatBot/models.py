from django.db import models
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _
from .constants import get_a_uuid


class Admin(models.Model):

    objects = models.Manager()

    name = models.CharField(max_length=100, null=False)
    mobile = models.BigIntegerField(null=False)
    email_id = models.EmailField(null=False)
    password = models.TextField(null=False)
    date_created = models.DateTimeField(null=False, blank=False)
    date_modified = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_logged_in = models.BooleanField(default=False)
    token = models.TextField(null=True, blank=True)
    token_expired = models.DateTimeField(null=True, blank=True)
    is_password_updated = models.BooleanField(default=False)

    class Meta:
        app_label = 'ChatBot'

    @property
    def full_name(self):
        """Returns the person's full name."""
        return '%s' % self.name


class Customers(models.Model):

    objects = models.Manager

    name = models.CharField(max_length=200, null=False)
    org_name = models.CharField(max_length=100, unique=True)
    web_url = models.TextField(unique=True)
    email_id = models.EmailField(
        max_length=200, null=False, blank=False, unique=True)
    mobile = models.BigIntegerField(null=False, blank=False, unique=True)
    password = models.TextField(null=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by_id = models.IntegerField(null=True)
    updated_by_id = models.IntegerField(null=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    logo_path = models.TextField(default='static/images/default/org_logo.png')
    last_login = models.DateTimeField(null=True, blank=True)
    is_logged_in = models.BooleanField(default=False)
    token = models.TextField(null=True, blank=True)
    token_expired = models.DateTimeField(null=True, blank=True)
    is_password_updated = models.BooleanField(default=False)

    class Meta:
        app_label = 'ChatBot'


class Bots(models.Model):

    objects = models.Manager

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True)
    model_name = models.CharField(max_length=125, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by_id = models.IntegerField(null=True)
    updated_by_id = models.IntegerField(null=True)

    class Meta:
        app_label = 'ChatBot'


class CustomerBots(models.Model):

    objects = models.Manager

    """
    name: string;
    title: string;
    server_IP: string;
    type: string;
    status: boolean;
    """
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    bot = models.ForeignKey(Bots, on_delete=models.CASCADE)
    customer_id_text = models.TextField(max_length=100, unique=True, default=get_a_uuid)
    bot_id_text = models.TextField(max_length=150, null=True, blank=True)
    source_url = models.TextField(unique=True)
    BOT_TYPE = Choices(
        ('BASIC', 'basic', _('BASIC')),
        ('POWER', 'power', _('POWER')),
    )
    bot_type = models.CharField(
        max_length=6,
        choices=BOT_TYPE
    )
    header_colour = models.CharField(max_length=25, default='#000000')
    body_colour = models.CharField(max_length=25, default='#FFFFFFF')
    font_type = models.CharField(max_length=25, default='Arial, Helvitica')
    bot_logo = models.TextField(default='static/images/default/bot_logo.png')
    chat_logo = models.TextField(default='static/images/default/chat.png')
    user_logo = models.TextField(default='static/images/default/user_logo.jpg')
    bot_bubble_colour = models.CharField(max_length=25, default='#C0C0C0')
    user_bubble_colour = models.CharField(max_length=25, default='#606060')
    chat_bot_font_colour = models.CharField(max_length=25, default='#000000')
    chat_user_font_colour = models.CharField(max_length=25, default='#FFFFFF')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by_id = models.IntegerField(null=True)
    updated_by_id = models.IntegerField(null=True)
    '''
    If for_whole_site is false, main domain of this
    source url may have multiple bots configuration.
    '''
    for_whole_site = models.BooleanField(default=False)

    class Meta:
        app_label = 'ChatBot'
        db_table = '%s_customer_bots' % app_label


class Conversation(models.Model):

    objects = models.Manager

    # ConversationRecordID
    bot = models.ForeignKey(Bots, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    bot_origin_url = models.TextField()
    ip_address = models.TextField(null=True)
    country = models.CharField(max_length=4, default='IN')
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


class BotConfiguration(models.Model):

    objects = models.Manager

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    bot = models.ForeignKey(Bots, on_delete=models.CASCADE)
    question = models.TextField(max_length=250)
    description = models.TextField(max_length=500, null=True, blank=True)
    question_id = models.IntegerField()  # UI Purpose
    ANSWER_TYPE = Choices(
        ('TEXT', 'text', _('TEXT')),
        ('NUMBER', 'number', _('NUMBER')),
        ('RADIO', 'radio', _('RADIO')),
        ('DROPDOWN', 'dropdown', _('DROPDOWN')),
        ('CHECKBOX', 'checkbox', _('CHECKBOX')),
        ('FILE', 'file', _('FILE')),
        ('DATE', 'date', _('DATE')),
        ('ACTION', 'action', _('ACTION')),
    )
    answer_type = models.CharField(max_length=10, choices=ANSWER_TYPE)
    suggested_answers = models.TextField(default=[{"payload": "", "title": ""}])
    suggested_jump = models.TextField(default=[])
    validation1 = models.TextField(null=True, blank=True)
    validation2 = models.TextField(null=True, blank=True)
    error_msg = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    required = models.CharField(max_length=4, default="no")
    related = models.BooleanField(default=True)
    is_first_question = models.BooleanField(default=False)
    is_last_question = models.BooleanField(default=False)
    is_lead_gen_question = models.BooleanField(default=False)
    validation_type = models.TextField(default='[]')
    number_of_params = models.IntegerField(default=0)
    fields = models.TextField(default='[]')
    api_name = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        app_label = 'ChatBot'
        db_table = '%s_client_questions' % app_label


class BulkQuestion(models.Model):
    mapping_id = models.ForeignKey(CustomerBots, on_delete=models.CASCADE, related_name='bulk_questions')
    questions = models.ManyToManyField(BotConfiguration)


class EmailStatus(models.Model):

    objects = models.Manager()

    id = models.AutoField(primary_key=True)
    template = models.TextField()
    context = models.TextField()
    recipient = models.TextField()
    subject = models.TextField()
    status = models.TextField()
    created_by_id = models.IntegerField()
    updated_by_id = models.IntegerField()
    date_created = models.DateTimeField(null=False, blank=False)
    date_modified = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        app_label = 'ChatBot'
        db_table = '%s_email_status' % app_label
