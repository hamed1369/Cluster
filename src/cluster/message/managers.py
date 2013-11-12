# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q
from cluster.message.actions import SendMessage, ShowMessage, SendEmail
from cluster.message.models import Message
from cluster.utils.forms import ClusterFilterModelForm
from cluster.utils.manager.action import DeleteAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class MessageFilterForm(ClusterFilterModelForm):
    body = forms.CharField(label=u"متن", required=False)
    status = forms.ChoiceField(label=u"نوع", choices=((u"1", u"دریافت شده"), (u"2", u"فرستاده شده"), (u"3", u"همه")),
                               initial=u"1", )

    class Meta:
        model = Message
        fields = ('title', 'body', 'sender')

    def __init__(self, *args, **kwargs):
        super(MessageFilterForm, self).__init__(*args, **kwargs)


class MessageManager(ObjectsManager):
    manager_name = u"messages"
    manager_verbose_name = u"جعبه پیام ها"
    filter_form = MessageFilterForm
    actions = [
        SendMessage(),
        DeleteAction(),
        ShowMessage(),
    ]
    filter_handlers = (
        ('title', 'str'),
        ('body', 'str'),
        ('sender', 'this'),
    )

    def __init__(self, http_request):
        super(MessageManager, self).__init__(http_request=http_request)
        if PermissionController.is_admin(http_request.user):
            self.actions = [
                SendMessage(),
                DeleteAction(),
                ShowMessage(),
                SendEmail(),
            ]

    def get_all_data(self):
        return Message.objects.filter(Q(receivers=self.http_request.user) | Q(sender=self.http_request.user))

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

    def other_filter_func(self, all_data, form):
        if form:
            form_data = form.data
            status = form_data.get('status')
            if status == u'2':
                all_data = all_data.filter(sender=self.http_request.user).distinct()
            elif status == u'3':
                pass
            else:
                all_data = all_data.filter(receivers=self.http_request.user).distinct()
        return all_data
