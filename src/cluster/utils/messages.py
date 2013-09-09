# -*- coding:utf-8 -*-
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.base import Template
from django.template.context import Context
from django.utils.safestring import mark_safe
from cluster import settings

__author__ = 'M.Y'


class MessageServices(object):
    from_email = u'موسسه‌پژوهشی‌نگاه‌نو'

    @staticmethod
    def send_message(subject, message, user, *args, **kwargs):
        try:
            msg = EmailMultiAlternatives(subject=subject, body='', from_email=MessageServices.from_email,
                                         to=[user.email])
            msg.attach_alternative(message, "text/html")
            msg.send()
            # send_mail(subject=subject, message=message, from_email=MessageServices.from_email,
            #           recipient_list=[user.email])
        except Exception as s:
            logging.error(s)

    @staticmethod
    def get_registration_message(cluster, user, username, password):

        url = settings.SITE_URL + u"/register/%s/" % cluster.id
        message = Template("""
            <div style="direction:rtl;">
            <h1>ثبت نام در خوشه {{cluster_name}} </h1>
            <p> {{name}} ،</p>
            <p>سلام</p>
            <p>
            شما توسط <b>{{head}}</b> به خوشه <b>{{cluster_name}}</b> دعوت شده اید.
            برای تکمیل فرایند ثبت نام به آدرس زیر مراجعه کرده و اطلاعات خود را تکمیل کنید.
            </p>
            نام کاربری شما: {{username}} <br/>
            گذرواژه شما: {{password}} <br/>
            لینک ثبت نام خوشه : {{url}} <br/>

            باتشکر<br/>
            موسسه پژوهشی نگاه نو
            </div>
        """).render(Context({
            'name': u"%s %s" % (user.first_name, user.last_name) if (
                user.first_name and user.last_name) else u"%s" % user.username,
            'head': unicode(cluster.head),
            'cluster_name': cluster.name,
            'url': url,
            'username': username,
            'password': password,
        }))
        return mark_safe(message)

    @staticmethod
    def get_delete_member_message(cluster, user):
        message = Template("""
                <div style="direction:rtl;">
                <h1>حذف از خوشه {{cluster_name}} </h1>
                <p> {{name}} ،</p>
                <p>سلام</p>
                <p>
                شما توسط <b>{{head}}</b> از خوشه <b>{{cluster_name}}</b> حذف شده اید.
                </p>

                باتشکر<br/>
                موسسه پژوهشی نگاه نو
                </div>
            """).render(Context({
            'name': u"%s %s" % (user.first_name, user.last_name) if (
                user.first_name and user.last_name) else u"%s" % user.username,
            'head': unicode(cluster.head),
            'cluster_name': cluster.name,
        }))
        return mark_safe(message)

    @staticmethod
    def get_send_message(sender, title, body):
        message = Template("""
                <div style="direction:rtl;">
                <h2> این پیام از طرف {{name}} برای شما ارسال شده است <h2>
                <h1>{{title}} </h1>
                <p> {{body}} ،</p>
                <p>
                شما توسط <b>{{head}}</b> از خوشه <b>{{cluster_name}}</b> حذف شده اید.
                </p>

                موسسه پژوهشی نگاه نو
                </div>
            """).render(Context({
            'name': u"%s %s" % (sender.first_name, sender.last_name) if (
                sender.first_name and sender.last_name) else u"%s" % sender.username,
            'title': title,
            'body': body
        }))
        return mark_safe(message)
