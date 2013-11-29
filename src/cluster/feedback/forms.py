# -*- coding: utf-8 -*-
from captcha.fields import CaptchaField
from django import forms
from cluster.feedback.models import Feedback, ContactUs
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


class ContactForm(ClusterBaseModelForm):
    class Meta:
        model = ContactUs

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['captcha'] = CaptchaField(label=u"کد امنیتی", error_messages={
            'invalid': u"کد امنیتی وارد شده صحیح نمی باشد."})
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': u'عنوان'})
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'placeholder': u'متن','cols':'10','rows':'5'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': u"پست الکترونیک"})
        self.fields['captcha'].widget.attrs.update({'class': 'form-control'})
        process_js_validations(self)


class ContactShowForm(FeedbackShowForm):
    class Meta:
        model = ContactUs