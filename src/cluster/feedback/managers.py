# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe
from cluster.feedback.forms import FeedbackShowForm
from cluster.feedback.models import Feedback
from cluster.message.actions import SendMessage, ShowMessage
from cluster.message.models import Message
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.action import DeleteAction, ShowAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn

__author__ = 'M.Y'


class FeedbackFilterForm(ClusterBaseModelForm):
    class Meta:
        model = Feedback
        fields = ('title', 'creator')


class MessageManager(ObjectsManager):
    manager_name = u"feedback_manager"
    manager_verbose_name = u"مشاهده نظرات و پیشنهادات"
    filter_form = FeedbackFilterForm
    actions = [
        DeleteAction(),
        ShowAction(FeedbackShowForm),
    ]

    def get_all_data(self):
        return Feedback.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", 7),
            ManagerColumn('body', u"متن", 20, True),
            ManagerColumn('creator', u"ایجادکننده", 3),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
        ]
        return columns

    def get_body(self, obj):
        body = obj.body.replace('\r\n', ' ').replace('\n\r', ' ').replace('\r', ' ').replace('\n', ' ')
        if len(body) > 45:
            body = body[:45] + ' ...'
        return body
