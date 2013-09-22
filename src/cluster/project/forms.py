# -*- coding:utf-8 -*-
from django import forms
from cluster.account.account.models import Domain
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
        exclude = ('single_member', 'cluster', 'project_status')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProjectForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.id and self.instance.confirmation_type != 1:
            self.fields['has_confirmation'].initial = True
        self.fields['confirmation_type'].choices = (
            (1, '---------'),
            (2, u"تاییدیه سازمان پژوهش های علمی و صنعتی ایران"),
            (3, u"برگزیده جشنواره خوارزمی"),
            (4, u"برگزیده جشنواره رازی"),
            (5, u"برگزیده جشنواره شیخ بهائی"),
            (6, u"برگزیده جشنواره فارابی"),
            (7, u"سایر دانشگاه ها و مراکز دولتی"),
        )
        self.fields['confirmation_type'].required = False
        self.fields['domain'].required = True
        self.fields['domain'].queryset = Domain.objects.filter(confirmed=True)
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
        if not cd.get('confirmation_type'):
            cd['confirmation_type'] = 1
        return cd

    def save(self, commit=True):
        instance = super(ProjectForm, self).save(commit)
        if self.user.member.cluster:
            instance.cluster = self.user.member.cluster
        else:
            instance.single_member = self.user.member
        instance.save()
        return instance


class ProjectManagerForm(ProjectForm):
    class Meta:
        model = Project
        exclude = ('single_member', 'cluster')

    def __init__(self, *args, **kwargs):
        kwargs['user'] = None
        super(ProjectManagerForm, self).__init__(*args, **kwargs)
        if 'agreement' in self.fields:
            del self.fields['agreement']
        self.fields.keyOrder = ['title', 'has_confirmation', 'confirmation_type', 'certificate_image', 'has_patent',
                                'patent_number', 'patent_date', 'patent_certificate', 'patent_request', 'domain',
                                'summary', 'keywords', 'innovations', 'state', 'project_status']
        process_js_validations(self)

    def save(self, commit=True):
        instance = super(ProjectForm, self).save(commit)
        return instance

