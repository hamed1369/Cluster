# -*- coding:utf-8 -*-
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.base import Template
from django.template.context import Context
from django.utils.safestring import mark_safe

__author__ = 'M.Y'


class MessageServices(object):
    from_email = u'info@persianelites.com'
    site_url = 'http://www.persianelites.com'

    @staticmethod
    def send_message(subject, message, user=None, *args, **kwargs):
        if user:
            email = user.email
        else:
            email = kwargs.get('email')
        try:
            msg = EmailMultiAlternatives(subject=subject, body='', from_email=MessageServices.from_email,
                                         to=[email])
            msg.attach_alternative(message, "text/html")
            msg.send()
            # send_mail(subject=subject, message=message, from_email=MessageServices.from_email,
            #           recipient_list=[user.email])
        except Exception as s:
            logging.error(s)

    @staticmethod
    def get_registration_message(cluster, user, username, password):
        url = MessageServices.site_url + u"/register/%s/" % cluster.id
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
                <p> {{body|safe}} ،</p>

                موسسه پژوهشی نگاه نو
                </div>
            """).render(Context({
            'name': u"%s %s" % (sender.first_name, sender.last_name) if (
                sender.first_name and sender.last_name) else u"%s" % sender.username,
            'title': title,
            'body': body.replace('\r\n', '<br/>').replace('\n\r', '<br/>').replace('\r', '<br/>').replace('\n', '<br/>')
        }))
        return mark_safe(message)

    @staticmethod
    def get_arbiter_invitation_message(title, message_txt, code):
        message = Template("""
                <div style="direction:rtl;">
                <p>
                    {{title}} ،
                    سلام
                    <br/>
                    شما به سامانه موسسه پژوهشی نگاه نو، به جهت داوری دعوت شده اید. برای تکمیل فرایند ثبت نام خود به آدرس زیر مراجعه کنید:
                    <br/>
                    {{link_url}}
                    <br/>
                    پیغام مدیر سامانه برای شما:
                    <br/>
                    {{message_txt|safe}}
                </p>

                موسسه پژوهشی نگاه نو
                </div>
            """).render(Context({
            'title': title,
            'link_url': u"%s/arbiter_register/?c=%s" % (MessageServices.site_url, code),
            'message_txt': message_txt.replace('\r\n', '<br/>').replace('\n\r', '<br/>').replace('\r', '<br/>').replace(
                '\n', '<br/>')

        }))
        return mark_safe(message)

    @staticmethod
    def get_title_body_message(title, body):
        message = Template("""
                <div style="direction:rtl;">
                <h1>{{title}} </h1>
                <p> {{body|safe}}</p>

                موسسه پژوهشی نگاه نو
                </div>
            """).render(Context({
            'title': title,
            'body': body.replace('\r\n', '<br/>').replace('\n\r', '<br/>').replace('\r', '<br/>').replace('\n', '<br/>')
        }))
        return mark_safe(message)


class SMSService(object):
    from_number = 30004934000555
    signature = u'موسسه پژوهشی نگاه نو'

    WSID = 1464
    username = 'tahmooresi'
    password = 44655288

    @classmethod
    def send_sms(cls, message, to_numbers):
        from suds.client import Client

        if not to_numbers:
            return
        if not to_numbers[0]:
            return

        message = message + '\n' + cls.signature

        try:
            client = Client(url="http://www.lpsms.ir/SMSWS/SOAPWebService.asmx?WSDL")
            numbers = client.factory.create('ArrayOfString')
            numbers.string = to_numbers
            params = {
                'WSID': cls.WSID,
                'UserName': cls.username,
                'Password': cls.password,
                'RecipientNumber': numbers,
                'MessageBody': message,
                'SpecialNumber': cls.from_number,
                'IsFlashMessage': False,

            }
            response = client.service.SendArray(**params)
            return response
        except Exception as s:
            logging.error(s)
