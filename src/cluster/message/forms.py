# -*- coding: utf-8 -*-
from cluster.message.models import Message
from cluster.utils.forms import ClusterBaseModelForm

__author__ = 'M.Y'


class MessageForm(ClusterBaseModelForm):
    class Meta:
        model = Message
        exclude = ('sender', 'state')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(MessageForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        message = super(MessageForm, self).save(commit=False)
        message.sender = self.user
        message.save()
        message.receivers = self.cleaned_data.get('receivers')
        return message


class MessageShowForm(ClusterBaseModelForm):
    class Meta:
        model = Message
        exclude = ('state', 'receivers')
