# -*- coding:utf-8 -*-
from django.core.mail import send_mail
from cluster import settings

__author__ = 'M.Y'


class MessageServices(object):
    from_email = 'a@b.co'

    REGISTRATION_MESSAGE = u"لینک ثبت نام خوشه : " + settings.SITE_URL + u"%s" + u"\n\r نام کاربری شما: %s \n\r گذرواژه شما: %s"

    @staticmethod
    def send_message(subject, message, users, *args, **kwargs):
        try:
            send_mail(subject=subject, message=message, from_email=MessageServices.from_email,
                      recipient_list=[user.email for user in users])
        except Exception as s:
            print s