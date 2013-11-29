# -*- coding:utf-8 -*-
from django.db import models

__author__ = 'Hourshad'

class IntroPageContent(models.Model):
    u"""
        محتوای صفحه اول
    """
    class Meta:
        verbose_name = u"محتوای صفحه اول"
        verbose_name_plural = u"محتوای صفحه اول"
        app_label = 'account'
    content = models.TextField(u"محتوای صفحه اول", max_length=5000)
    instance = None

    @staticmethod
    def get_instance():
        if IntroPageContent.instance:
            return IntroPageContent.instance
        try:
            return IntroPageContent.objects.all()[0]
        except IndexError:
            return IntroPageContent.objects.create(content= " ")