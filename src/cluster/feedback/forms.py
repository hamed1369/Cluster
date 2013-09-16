# -*- coding: utf-8 -*-
from django import forms
from cluster.feedback.models import Feedback
from cluster.utils.date import handel_date_fields
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.js_validation import process_js_validations

__author__ = 'M.Y'


class FeedbackForm(ClusterBaseModelForm):
    class Meta:
        model = Feedback
        exclude = ('creator',)


class FeedbackShowForm(ClusterBaseModelForm):
    class Meta:
        model = Feedback

    def __init__(self, *args, **kwargs):
        super(FeedbackShowForm, self).__init__(*args, **kwargs)
        self.fields['created_on'] = forms.DateField(label=u"تاریخ ایجاد")
        self.fields['created_on'].initial = self.instance.created_on
        handel_date_fields(self)
        process_js_validations(self)