# -*- coding: utf-8 -*-
from django import forms
from tinymce.widgets import TinyMCE
from cluster.news.models import News, Link
from cluster.utils.date import handel_date_fields
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.js_validation import process_js_validations

__author__ = 'M.Y'


class NewsForm(ClusterBaseModelForm):
    class Meta:
        model = News
        exclude = ('creator',)
    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = TinyMCE(attrs={'cols': 60, 'rows': 20})


class NewsShowForm(ClusterBaseModelForm):

    class Meta:
        model = News

    def __init__(self, *args, **kwargs):
        super(NewsShowForm, self).__init__(*args, **kwargs)
        self.fields['created_on'] = forms.DateField(label=u"تاریخ ایجاد")
        self.fields['created_on'].initial = self.instance.created_on
        self.fields['body'].widget = TinyMCE(attrs={'cols': 60, 'rows': 20})
        handel_date_fields(self)
        process_js_validations(self)


class LinkForm(ClusterBaseModelForm):
    class Meta:
        model = Link


class LinkShowForm(NewsShowForm):
    class Meta:
        model = Link
