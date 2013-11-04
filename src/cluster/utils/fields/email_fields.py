# -*- coding:utf-8 -*-

__author__ = 'M.Y'
import re

from django.core.validators import email_re
from django.forms import CharField, Textarea, ValidationError


email_separator_re = re.compile(r'[,;\n\r]+')


def _is_valid_email(email):
    return email_re.match(email.strip(' \n\r'))


class EmailsListField(CharField):
    widget = Textarea

    def clean(self, value):
        super(EmailsListField, self).clean(value)

        value = value.strip(' \n\r')

        emails = email_separator_re.split(value)

        if not emails:
            raise ValidationError(u"حداقل یک پست الکترونیک را وارد نمایید.")

        for email in emails:
            if not _is_valid_email(email):
                raise ValidationError(u'%s یک آدرس پست الکترونیک صحیح نیست.' % email)

        return emails