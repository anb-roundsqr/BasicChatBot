from django.db import models
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _


class ClientQuestions(models.Model):

    objects = models.Manager

    id = models.AutoField(primary_key=True)
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
    created_by_id = models.IntegerField()
    updated_by_id = models.IntegerField()
    date_created = models.DateTimeField(null=False, blank=False)
    date_modified = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    required = models.CharField(max_length=4, default="no")

    class Meta:
        app_label = 'ChatBot'
        db_table = '%s_client_questions' % app_label
