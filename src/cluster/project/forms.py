# -*- coding:utf-8 -*-
from django import forms
from cluster.project.models import Project
from cluster.utils.fields import BOOLEAN_CHOICES
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.js_validation import process_js_validations

__author__ = 'M.Y'


class ProjectForm(ClusterBaseModelForm):
    has_confirmation = forms.ChoiceField(required=True, choices=BOOLEAN_CHOICES,
                                         widget=forms.RadioSelect(),
                                         label=u"آیا طرح دارای تاییدیه علمی و نوآوری از مراجع می باشد?",
                                         help_text=u"تأئيديه سازمان پژوهشهای علمی و صنعتی ايران، برگزيده جشنواره خوارزمی، برگزيده جشنواره رازی، برگزيده جشنواره شیخ بهائی، برگزيده جشنواره فارابی، سایر دانشگاه ها و مراکز دولتی، همراه با تصوریری از مدرک", )

    class Meta:
        model = Project

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['confirmation_type'].choices = (
            ('', '---------'),
            (2, u"تاییدیه سازمان پژوهش های علمی و صنعتی ایران"),
            (3, u"برگزیده جشنواره خوارزمی"),
            (4, u"برگزیده جشنواره رازی"),
            (5, u"برگزیده جشنواره شیخ بهائی"),
            (6, u"برگزیده جشنواره فارابی"),
            (7, u"سایر دانشگاه ها و مراکز دولتی"),
        )
        self.fields['confirmation_type'].required = False
        self.fields['domain'].required = True
        self.fields['has_patent'] = forms.ChoiceField(required=True, choices=BOOLEAN_CHOICES,
                                                      widget=forms.RadioSelect(), )
        self.fields['has_patent'].label = u"آیا طرح پیشنهادی دارای ثبت اختراع می باشد؟"

        self.fields['patent_request'] = forms.ChoiceField(required=True, choices=BOOLEAN_CHOICES,
                                                          widget=forms.RadioSelect(), )
        self.fields['patent_request'].label = u"آیا صاحب طرح متقاضی ثبت اختراع می باشد؟"

        self.fields['summary'].widget = forms.Textarea()

        self.fields['agreement'] = forms.BooleanField(required=True)
        self.fields[
            'agreement'].label = u"اينجانب با اطلاع کامل از رويه‌ها و ضوابط ارائه اختراع، اين پرسشنامه را تکميل نموده و کليه اطلاعات مندرج در آن را تأئيد مي‌نمايم. مسئوليت هرگونه نقص يا اشتباه در اطلاعات ارسالي به عهده اينجانب است."

        process_js_validations(self)

    def clean(self):
        cd = super(ProjectForm, self).clean()
        return cd


class ProjectManagerForm(ProjectForm):
    def __init__(self, *args, **kwargs):
        super(ProjectManagerForm, self).__init__(*args, **kwargs)
        if 'agreement' in self.fields:
            del self.fields['agreement']
        self.fields.keyOrder = ['title', 'has_confirmation', 'confirmation_type', 'certificate_image', 'has_patent', 'patent_number', 'patent_date', 'patent_certificate', 'patent_request', 'domain', 'summary', 'keywords', 'innovations', 'state', 'project_status']
        process_js_validations(self)