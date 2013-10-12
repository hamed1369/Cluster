# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from cluster.account.account.models import Cluster
from cluster.message.models import Message
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.js_validation import process_js_validations
from cluster.utils.messages import MessageServices
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class AdminMessageForm(ClusterBaseModelForm):
    SEND_TYPE = (
        (1, u"ارسال به همه"),
        (2, u"ارسال به همه اعضا خوشه ها"),
        (3, u"ارسال به همه  سر خوشه ها"),
        (4, u"ارسال به برخی از اعضا خوشه ها"),
        (5, u"ارسال به همه داوران"),
        (6, u"ارسال به برخی داوران"),
    )

    class Meta:
        model = Message
        exclude = ('sender', 'state')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AdminMessageForm, self).__init__(*args, **kwargs)
        self.fields['send_type'] = forms.ChoiceField(label=u"نوع گیرنده", choices=AdminMessageForm.SEND_TYPE)
        self.fields['send_type'].required = False
        self.fields['receivers'].queryset = PermissionController.get_available_receivers(self.user)
        self.fields['receivers'].required = False
        process_js_validations(self)
        self.fields['send_type'].required = True
        self.fields.keyOrder = ['title', 'body', 'send_type', 'receivers']

    def save(self, commit=True):
        message = super(AdminMessageForm, self).save(commit=False)
        message.sender = self.user
        message.save()

        send_type = int(self.cleaned_data.get('send_type'))

        if send_type == 1:
            receivers = User.objects.all()
        elif send_type == 2:
            receivers = User.objects.filter(member__isnull=False)
        elif send_type == 3:
            receivers = Cluster.objects.filter().values_list('head', flat=True)
        elif send_type == 5:
            receivers = User.objects.filter(arbiter__isnull=False)
        else:
            receivers = self.cleaned_data.get('receivers')

        message.receivers = receivers

        if receivers:
            for user in receivers:
                message_text = MessageServices.get_send_message(self.user, message.title, message.body)
                MessageServices.send_message(subject=u"پیام دریافتی از مدیریت سیستم",
                                             message=message_text, user=user)
        return message


class ArbiterMessageForm(ClusterBaseModelForm):
    class Meta:
        model = Message
        exclude = ('sender', 'state', 'receivers')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ArbiterMessageForm, self).__init__(*args, **kwargs)
        self.fields['send_type'] = forms.BooleanField(label=u"ارسال پیام به مدیر سیستم",
                                                      widget=forms.CheckboxInput(
                                                          {'readonly': 'readonly', 'disabled': 'disabled'}),
                                                      initial=True, required=False)
        process_js_validations(self)

    def save(self, commit=True):
        message = super(ArbiterMessageForm, self).save(commit=False)
        message.sender = self.user
        message.save()

        receivers = PermissionController.get_admins()
        message.receivers = receivers
        if receivers:
            for user in receivers:
                message_text = MessageServices.get_send_message(self.user, message.title, message.body)
                MessageServices.send_message(subject=u"پیام دریافتی سامانه",
                                             message=message_text, user=user)
        return message


class MemberMessageForm(ClusterBaseModelForm):
    SEND_TYPE = (
        (7, u"ارسال به مدیر سیستم"),
        (8, u"ارسال به همه اعضا خوشه"),
        (9, u"ارسال به بعضی اعضا خوشه"),
    )

    class Meta:
        model = Message
        exclude = ('sender', 'state')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(MemberMessageForm, self).__init__(*args, **kwargs)
        self.fields['send_type'] = forms.ChoiceField(label=u"نوع گیرنده", choices=MemberMessageForm.SEND_TYPE)
        self.fields['send_type'].required = False
        self.fields['receivers'].queryset = PermissionController.get_available_receivers(self.user)
        self.fields['receivers'].required = False
        process_js_validations(self)
        self.fields['send_type'].required = True
        self.fields.keyOrder = ['title', 'body', 'send_type', 'receivers']

    def save(self, commit=True):
        message = super(MemberMessageForm, self).save(commit=False)
        message.sender = self.user
        message.save()

        send_type = int(self.cleaned_data.get('send_type'))

        if send_type == 7:
            receivers = PermissionController.get_admins()
        elif send_type == 8:
            receivers = User.objects.filter(member__in=self.user.cluster.members.filter().distinct())
            #receivers = self.user.member.cluster.members.filter().values_list('user', flat=True)
        else:
            receivers = self.cleaned_data.get('receivers')

        message.receivers = receivers

        if receivers:
            for user in receivers:
                message_text = MessageServices.get_send_message(self.user, message.title, message.body)
                MessageServices.send_message(subject=u"پیام دریافتی سامانه",
                                             message=message_text, user=user)
        return message


class MessageShowForm(ClusterBaseModelForm):
    class Meta:
        model = Message
        exclude = ('state', 'receivers')
