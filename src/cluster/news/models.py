# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

__author__ = 'M.Y'
from django.db import models


class News(models.Model):
    title = models.CharField(verbose_name=u"عنوان", max_length=255)
    body = models.TextField(verbose_name=u"متن", max_length=1000)
    creator = models.ForeignKey(User, verbose_name=u"ایجادکننده", related_name='news')
    created_on = models.DateField(verbose_name=u"تاریخ ایجاد", auto_now_add=True)
    publish_date = models.DateField(verbose_name=u"تاریخ انتشار")

    class Meta:
        app_label = 'news'
        verbose_name = u"خبر"
        verbose_name_plural = u"اخبار"

    def __unicode__(self):
        return u"%s" % self.title


    @staticmethod
    def create_news(user, title, body, publish_date):
        news = News.objects.create(title=title, body=body, creator=user, publish_date=publish_date)
        return news
