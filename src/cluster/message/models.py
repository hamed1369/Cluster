# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

__author__ = 'M.Y'
from django.db import models


class Message(models.Model):
    READ = 1
    UNREAD = 2
    MESSAGE_STATES = (
        (1, u"خوانده شده"),
        (2, u"خوانده نشده")
    )
    title = models.CharField(verbose_name=u"عنوان", max_length=255)
    body = models.TextField(verbose_name=u"متن پیام", max_length=1000)
    sender = models.ForeignKey(User, verbose_name=u"فرستنده", related_name='messages_as_sender')
    receivers = models.ManyToManyField(User, verbose_name=u"گیرنده ها", related_name='messages_as_receiver')
    state = models.IntegerField(verbose_name=u"وضعیت", choices=MESSAGE_STATES, default=UNREAD)

    class Meta:
        app_label = 'message'
        verbose_name = u"پیام"
        verbose_name_plural = u"پیام ها"

    def __unicode__(self):
        return u"%s : %s to %s" % (self.title, self.sender, ','.join([unicode(x) for x in self.receivers.all()]))

    @staticmethod
    def get_user_messages(user):
        return Message.objects.filter(receivers=user)

    @staticmethod
    def send_message(user, title, body, receivers):
        message = Message.objects.create(title=title, body=body, sender=user, receivers=receivers)
        return message
