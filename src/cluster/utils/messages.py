# -*- coding:utf-8 -*-
import logging
from django.core.mail import send_mail
from django.template.base import Template
from django.template.context import Context
from django.utils.safestring import mark_safe
from cluster import settings

__author__ = 'M.Y'


class MessageServices(object):
    from_email = 'a@b.co'

    @staticmethod
    def send_message(subject, message, user, *args, **kwargs):
        try:
            send_mail(subject=subject, message=message, from_email=MessageServices.from_email,
                      recipient_list=[user.email])
        except Exception as s:
            logging.error(s)


    @staticmethod
    def get_registration_message(cluster, username, password):

        url = settings.SITE_URL + u"/register/%s/" % cluster.id
        message = Template("""
            <h1>ثبت نام در خوشه {{cluster_name}} </h1>
            <h3>باسلام</h3>
            <p>
            شما به عنوان عضو خوشه {{cluster_name}} معرفی شده اید.
            برای تکمیل ثبت نام خود با استفاده از نام کاربری و گذرواژه زیر به لینک ثبت نام خوشه مراجعه فرمایید.
            </p>
            لینک ثبت نام خوشه : {{url}} <br/>
            نام کاربری شما: {{username}} <br/>
            گذرواژه شما: {{password}} <br/>

            باتشکر
        """).render(Context({
            'cluster_name': cluster.name,
            'url': url,
            'username': username,
            'password': password,
        }))
        return mark_safe(message)

