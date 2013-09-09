# -*- coding: utf-8 -*-
from cluster.message.models import Message
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.messages import MessageServices
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class MessageForm(ClusterBaseModelForm):
    class Meta:
        model = Message
        exclude = ('sender', 'state')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['receivers'].queryset = PermissionController.get_available_receivers(self.user)

    def save(self, commit=True):
        message = super(MessageForm, self).save(commit=False)
        message.sender = self.user
        message.save()
        message.receivers = self.cleaned_data.get('receivers')
        if self.cleaned_data.get('receivers'):
            for user in self.cleaned_data.get('receivers'):
                message = MessageServices.get_send_message(self.user, message.title, message.body)
                MessageServices.send_message(subject=u"پیام دریافتی سامانه",
                                             message=message,user=user)

        return message


class MessageShowForm(ClusterBaseModelForm):
    class Meta:
        model = Message
        exclude = ('state', 'receivers')
