# -*- coding:utf-8 -*-
from cluster.utils.date import handel_date_fields
from cluster.utils.js_validation import process_js_validations
from cluster.utils.widgets.phone import handle_phone_fields

__author__ = 'M.Y'
from django import forms
import re

not_persian_re = re.compile("[u\0600-u\06FF]+")


class ClusterBaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(ClusterBaseForm, self).__init__(*args, **kwargs)
        handel_date_fields(self)
        process_js_validations(self)
        handle_phone_fields(self)

    def clean(self):
        cd = super(ClusterBaseForm, self).clean()
        for field in self.fields:
            if isinstance(self.fields[field], forms.FileField):
                val = cd.get(field)
                if val:
                    val = val.name
                    if not not_persian_re.match(val):
                        self._errors[field] = self.error_class(
                            [u"لطفا در ثبت فایل ها فقط از کارکترهای انگلیسی استفاده کنید."])
        return cd


class ClusterBaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(ClusterBaseModelForm, self).__init__(*args, **kwargs)
        handel_date_fields(self)
        process_js_validations(self)
        handle_phone_fields(self)

    def clean(self):
        cd = super(ClusterBaseModelForm, self).clean()
        for field in self.fields:
            if isinstance(self.fields[field], forms.FileField):
                val = cd.get(field)
                if val:
                    val = val.name
                    if not not_persian_re.match(val):
                        self._errors[field] = self.error_class(
                            [u"لطفا در ثبت فایل ها فقط از کارکترهای انگلیسی استفاده کنید."])
        return cd


class ClusterFilterModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(ClusterFilterModelForm, self).__init__(*args, **kwargs)
        handel_date_fields(self)
        process_js_validations(self)

