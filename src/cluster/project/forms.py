# -*- coding:utf-8 -*-
from django import forms
from cluster.account.account.models import Domain, Arbiter, Member
from cluster.project.models import Project, ProjectMilestone, ProjectArbiter
from cluster.utils.fields import BOOLEAN_CHOICES
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.js_validation import process_js_validations

__author__ = 'M.Y'


class ProjectForm(ClusterBaseModelForm):
    has_confirmation = forms.ChoiceField(required=True, choices=BOOLEAN_CHOICES,
                                         widget=forms.RadioSelect(), initial=False,
                                         label=u"آیا طرح دارای تاییدیه علمی و نوآوری از مراجع می باشد؟",
                                         help_text=u"تأئيديه سازمان پژوهشهای علمی و صنعتی ايران، برگزيده جشنواره خوارزمی، برگزيده جشنواره رازی، برگزيده جشنواره شیخ بهائی، برگزيده جشنواره فارابی، سایر دانشگاه ها و مراکز دولتی، همراه با تصوریری از مدرک", )

    class Meta:
        model = Project
        exclude = ('single_member', 'cluster', 'project_status', 'score', 'supervisor')

    js_validation_configs = {
        'excludes_required': 'attended_members'
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProjectForm, self).__init__(*args, **kwargs)
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
                                                      widget=forms.RadioSelect(), initial=False)
        self.fields['has_patent'].label = u"آیا طرح پیشنهادی دارای ثبت اختراع می باشد؟"
        if self.instance and self.instance.id:
            if self.instance.confirmation_type != 1:
                self.fields['has_confirmation'].initial = True
            else:
                self.fields['has_confirmation'].initial = False
                self.fields['confirmation_type'].is_hidden = True
                self.fields['certificate_image'].is_hidden = True
            if not self.instance.has_patent:
                self.fields['patent_number'].is_hidden = True
                self.fields['patent_date'].is_hidden = True
                self.fields['patent_certificate'].is_hidden = True

        self.fields['patent_request'] = forms.ChoiceField(required=True, choices=BOOLEAN_CHOICES,
                                                          widget=forms.RadioSelect(),initial=False )
        self.fields['patent_request'].label = u"آیا صاحب طرح متقاضی ثبت اختراع می باشد؟"

        self.fields['summary'].widget = forms.Textarea()
        if self.user and self.user.member and self.user.member.cluster:
            self.fields['attended_members'].queryset = Member.objects.filter(cluster=self.user.member.cluster)
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
        exclude = ('single_member', 'cluster', 'score', 'supervisor')

    def __init__(self, *args, **kwargs):
        kwargs['user'] = None
        super(ProjectManagerForm, self).__init__(*args, **kwargs)
        if 'agreement' in self.fields:
            del self.fields['agreement']
        self.fields.keyOrder = ['title', 'has_confirmation', 'confirmation_type', 'certificate_image', 'has_patent',
                                'patent_number', 'patent_date', 'patent_certificate', 'patent_request', 'domain',
                                'summary', 'keywords', 'innovations', 'state', 'attended_members', 'project_status']
        process_js_validations(self)

    def save(self, commit=True):
        instance = super(ProjectForm, self).save(commit)
        return instance


class ArbiterProjectManagerForm(ProjectManagerForm):
    class Meta:
        model = Project
        exclude = ('single_member', 'cluster', 'score', 'project_status', 'supervisor')

    def __init__(self, *args, **kwargs):
        kwargs['user'] = None
        super(ProjectManagerForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['title', 'has_confirmation', 'confirmation_type', 'certificate_image', 'has_patent',
                                'patent_number', 'patent_date', 'patent_certificate', 'patent_request', 'domain',
                                'summary', 'keywords', 'innovations', 'state', 'attended_members']
        process_js_validations(self)


class AdminProjectManagerForm(ProjectManagerForm):
    class Meta:
        model = Project
        exclude = ('single_member', 'cluster')

    extra_js_validation = {
        'score': 'required',
    }

    def __init__(self, *args, **kwargs):
        kwargs['user'] = None
        super(AdminProjectManagerForm, self).__init__(*args, **kwargs)
        if 'agreement' in self.fields:
            del self.fields['agreement']
        self.fields.keyOrder = ['title', 'has_confirmation', 'confirmation_type', 'certificate_image', 'has_patent',
                                'patent_number', 'patent_date', 'patent_certificate', 'patent_request', 'domain',
                                'summary', 'keywords', 'innovations', 'supervisor', 'state', 'attended_members',
                                'project_status', 'score']
        if self.instance and self.instance.id:
            if self.instance.project_status != 1:
                self.fields['score'].is_hidden = True
        self.fields['project_status'].choices = (
            (-1, u"رد شده"),
            (0, u"در مرحله درخواست"),
            (1, u"تایید مرحله اول"),
            #(2, u"تاییدشده توسط داور"),
            (3, u"تایید مرحله دوم"),
            (4, u"تکمیل شده"),

        )
        process_js_validations(self)

    def clean(self):
        cd = super(AdminProjectManagerForm, self).clean()
        project_status = cd.get('project_status')
        if project_status == 1:
            if not cd.get('score'):
                self.errors['score'] = self.error_class([u"در تایید مرحله اول باید امتیاز مشخص شود."])
        return cd


class MilestoneForm(ClusterBaseModelForm):
    js_validation_configs = {
        'required': False,
    }

    class Meta:
        model = ProjectMilestone
        exclude = ('is_announced',)


class ProjectArbiterForm(ClusterBaseModelForm):
    js_validation_configs = {
        'required': False,
    }

    class Meta:
        model = ProjectArbiter
        exclude = (
            'confirm_date', 'economic_comment', 'innovation_comment', 'time_comment', 'budget_comment', 'attachment',
            'confirmed'
        )

    def __init__(self, *args, **kwargs):
        super(ProjectArbiterForm, self).__init__(*args, **kwargs)
        self.fields['arbiter'].queryset = Arbiter.objects.filter(invited=False)


class ProjectArbitrationForm(ClusterBaseModelForm):
    class Meta:
        model = ProjectArbiter
        exclude = ('confirm_date', 'arbiter', 'project')

    def __init__(self, *args, **kwargs):
        super(ProjectArbitrationForm, self).__init__(*args, **kwargs)