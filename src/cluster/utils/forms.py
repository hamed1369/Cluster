# -*- coding:utf-8 -*-
from cluster.utils.date import handel_date_fields
from cluster.utils.js_validation import process_js_validations
from cluster.utils.widgets.phone import handle_phone_fields

__author__ = 'M.Y'
from django import forms


class ClusterBaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(ClusterBaseForm, self).__init__(*args, **kwargs)
        handel_date_fields(self)
        process_js_validations(self)
        handle_phone_fields(self)


class ClusterBaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(ClusterBaseModelForm, self).__init__(*args, **kwargs)
        handel_date_fields(self)
        process_js_validations(self)
        handle_phone_fields(self)


class ClusterFilterModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if 'http_request' in kwargs:
            self.http_request = kwargs.pop('http_request')
        super(ClusterFilterModelForm, self).__init__(*args, **kwargs)
        handel_date_fields(self)
        process_js_validations(self)

