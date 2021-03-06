# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.template.base import Template
from django.template.context import Context, RequestContext
from cluster.account.templatetags.date_template_tags import pdate

__author__ = 'M.Y'
from django.db import models


class News(models.Model):
    title = models.CharField(verbose_name=u"عنوان", max_length=255)
    body = models.CharField(verbose_name=u"متن", max_length=10000)
    creator = models.ForeignKey(User, verbose_name=u"ایجادکننده", related_name='news')
    created_on = models.DateField(verbose_name=u"تاریخ ایجاد", auto_now_add=True)
    publish_date = models.DateField(verbose_name=u"تاریخ انتشار")
    archived = models.BooleanField(verbose_name=u"آرشیو",default=False)
    class Meta:
        app_label = 'news'
        verbose_name = u"خبر"
        verbose_name_plural = u"اخبار"

    def __unicode__(self):
        return u"%s" % self.title

    @staticmethod
    def get_html():
        news_list = News.objects.filter(archived=False).order_by('-publish_date')
        res = Template(u"""
            <table style="width: 100%">
            {% for item in news_list %}
                <tr><td style="width: 80%;"><a href="/news/{{ item.id }}/">{{ item.title }}</a></td><td>{{ item.publish_date_pdate }}</td></tr>
            {% empty %}
                <p>خبری یافت نشد.</p>
            {% endfor %}
            </table>
        """).render(Context({'news_list': news_list}))
        return res

    def publish_date_pdate(self):
        if isinstance(self.publish_date,str):
            return "none"
        return pdate(self.publish_date)

    @staticmethod
    def create_news(user, title, body, publish_date):
        news = News.objects.create(title=title, body=body, creator=user, publish_date=publish_date)
        return news


class Link(models.Model):
    title = models.CharField(verbose_name=u"عنوان", max_length=255)
    url = models.URLField(verbose_name=u"لینک")
    order = models.PositiveIntegerField(verbose_name=u"ترتیب نمایش", default=1)
    created_on = models.DateField(verbose_name=u"تاریخ ایجاد", auto_now_add=True)

    class Meta:
        app_label = 'news'
        verbose_name = u"لینک"
        verbose_name_plural = u"لینک ها"

    def __unicode__(self):
        return u"%s" % self.title

    @staticmethod
    def get_links_content(request):
        links_list = Link.objects.all().order_by('order')
        template = Template("""
            <table>
                {% for item in links_list %}
                    {% cycle '<tr><td>' '<td>'%}  <a href="{{ item.url }}">{{ item.title }}</a> {% cycle '</td>' '</td></tr>' %}
                {% empty %}
                    <p>پیوندی یافت نشد.</p>
                {% endfor %}
            </table>
        """)
        return template.render(RequestContext(request,{'links_list':links_list}))


class File(models.Model):
    file = models.FileField(u"فایل",upload_to='attachments/')


    class Meta:
        app_label = 'news'
        verbose_name = u"فایل"
        verbose_name_plural = u"فایل ها"


    def __unicode__(self):
        return self.file.url