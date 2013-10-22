# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe
from cluster.message.actions import SendMessage, ShowMessage
from cluster.message.models import Message
from cluster.utils.forms import ClusterBaseModelForm, ClusterFilterModelForm
from cluster.utils.manager.action import DeleteAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn

__author__ = 'M.Y'


class MessageFilterForm(ClusterFilterModelForm):
    body = forms.CharField(label=u"متن", required=False)

    class Meta:
        model = Message
        fields = ('title', 'body', 'sender')


class MessageManager(ObjectsManager):
    manager_name = u"messages"
    manager_verbose_name = u"جعبه پیام ها"
    filter_form = MessageFilterForm
    actions = [
        SendMessage(),
        DeleteAction(),
        ShowMessage(),
    ]

    def get_all_data(self):
        return Message.get_user_messages(self.http_request.user)

    def get_columns(self):
        columns = [
            ManagerColumn('sender', u"فرستنده", 5),
            ManagerColumn('title', u"عنوان", 7),
            ManagerColumn('body', u"متن", 20, True),
            # ManagerColumn('state', u"خوانده شده", 3, True),
        ]
        return columns

    def get_body(self, obj):
        body = obj.body.replace('\r\n', ' ').replace('\n\r', ' ').replace('\r', ' ').replace('\n', ' ')
        if len(body) > 45:
            body = body[:45] + ' ...'
        return body

    def get_state(self, obj):
        state = obj
        if state == Message.READ:
            return u"بله"
            # result = u'<img src="/static/manager/images/read.png" />'
        else:
            return u"خیر"
            # result = u'<img src="/static/manager/images/unread.png" />'
        return mark_safe(result)