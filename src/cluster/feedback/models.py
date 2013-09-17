# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

__author__ = 'M.Y'
from django.db import models


class Feedback(models.Model):
    title = models.CharField(verbose_name=u"عنوان", max_length=255)
    body = models.TextField(verbose_name=u"متن", max_length=1000)
    creator = models.ForeignKey(User, verbose_name=u"ایجادکننده", related_name='feedback')
    created_on = models.DateField(verbose_name=u"تاریخ ایجاد", auto_now_add=True)

    class Meta:
        app_label = 'feedback'
        verbose_name = u"انتقاد و پیشنهاد"
        verbose_name_plural = u"انتقادات و پیشنهادات"

    def __unicode__(self):
        return u"%s" % self.title

    @staticmethod
    def get_user_feedback(user):
        return Feedback.objects.filter(creator=user)

    @staticmethod
    def send_feedback(user, title, body):
        message = Feedback.objects.create(title=title, body=body, creator=user)
        return message
