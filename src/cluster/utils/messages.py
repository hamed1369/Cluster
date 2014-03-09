# -*- coding:utf-8 -*-
import logging
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.base import Template
from django.template.context import Context
from django.utils.safestring import mark_safe

__author__ = 'M.Y'


class MessageServices(object):
    from_email = u'noreply@persianelites.com'
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
    def send_mass_message(subject, body, receivers,email=None):
        try:
            msg_body = """
                <div style="font-family: tahoma, sans-serif;font-size: 12px;text-align: right;direction: rtl;">
                    %s
                </div>
            """ % body
            if not email:
                email = MessageServices.from_email
            connection = get_connection(username=None,
                                        password=None,
                                        fail_silently=None)
            message = EmailMultiAlternatives(subject=subject, body='', from_email=email,
                                             bcc=receivers, )
            message.attach_alternative(msg_body, 'text/html')
            messages = [message]
            return connection.send_messages(messages)
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
                شما  از خوشه <b>{{cluster_name}}</b> حذف شده اید.
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
    def get_arbiter_invitation_message(title, code):
        message = Template("""
                <div style="direction:rtl;">
                <p>
                    {{title}} ،
                    سلام
                    <br/>
                    <p>با تشکر از حسن توجه جنابعالی نسبت به همکاری با موسسه پژوهشی نگاه نو، از شما تقاضا می شود جهت تکمیل اطلاعات خود در سامانه این موسسه به لینک زیر مراجعه نمایید. امیدواریم همکاری های متقابل این موسسه با شما و بهره مندی از تخصص حضرتعالی سبب رسیدن به هدف متعالی ترسیم شده برای موسسه گردد.</p>
                    <br/>
                    {{link_url}}
                    <br/>
                    <p>لازم به ذکر است کلیه فرایند داوری بصورت الکترونیکی و از طریق سامانه موسسه قابل پیگیری می باشد. </p>
                    <p>مراحل داوری:</p>
                    <ol>
                        <li>در ابتدا صفحه ای با عنوان ثبت اطلاعات فردی ظاهر خواهد شد که بعد از ثبت اطلاعات (حداقل موارد ضروری) فرایند ثبت حضرتعالی در سامانه تثبیت خواهد شد. جهت مراجعه مجدد به پروفایل شخصی خود بعد از ورود به سایت اصلی موسسه از نام کاربری و گذرواژه وارد شده توسط خود، استفاده نمایید.</li>
                        <li>بعد از آن تمامی طرح های ارسالی از سوی موسسه در پروفایل شخصی شما قابل پیگیری خواهد بود. لازم است جهت انجام فرایند داوری، فرم مربوطه که در قالب فایل Word می باشد به همراه فایل طرح پیاده سازی شود.</li>
                        <li>سامانه بطور خودکار بعد از ارسال طرح، اقدام به تهیه قرارداد داوری خواهد نمود که بر اساس زمانبندی و قوانین موسسه حداکثر 2 هفته کاری، مدت زمان تخمینی جهت انجام داوری طرح ارسالی می باشد. </li>
                        <li>جهت امضا قرارداد، هماهنگی های لازم از طریق سامانه و یا تماس تلفنی امکان پذیر خواهد بود.</li>
                        <li>بعد از اتمام مدت زمان داوری (2هفته) و ارسال فرم داوری تکمیل شده از سوی جنابعالی، ادامه فرایند حمایتی طرح از طریق موسسه قابل پیگیری می باشد.  </li>
                    </ol>
                    <br/>

                </p>
                باتشکر
                </br>
                موسسه پژوهشی نگاه نو
                </div>
            """).render(Context({
            'title': title,
            'link_url': u"%s/arbiter_register/?c=%s" % (MessageServices.site_url, code),

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

        for i in range(len(to_numbers)):
            to_numbers[i] = '+' + to_numbers[i].replace('-', '')

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
