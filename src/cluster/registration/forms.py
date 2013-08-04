# -*- coding:utf-8 -*-
from django import forms
from cluster.account.account.models import Member
from cluster.account.personal_info.models import EducationalResume, Publication, Invention, \
    ExecutiveResearchProject, LanguageSkill, SoftwareSkill

__author__ = 'M.Y'


class ClusterForm(forms.Form):
    BOOLEAN_CHOICES = (
        (1, u"بله"),
        (1, u"خیر"),
    )
    is_cluster = forms.ChoiceField(required=False, choices=BOOLEAN_CHOICES, widget=forms.RadioSelect(),
                                   label=
                                   u"آیا درخواست ثبت خوشه وجود دارد؟(در صورت تایید و ارسال فرم ثبت نام برای اعضاء خوشه)",
    )

    def __init__(self, *args, **kwargs):
        super(ClusterForm, self).__init__(*args, **kwargs)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ('cluster', 'user')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs.update({'class': 'validate[required,] text-input'})


class MemberForm(forms.Form):
    name = forms.CharField(label=u"نام و نام خانوادگی")
    email = forms.EmailField(label=u"پست الکترونیک")


class EducationalResumeForm(forms.ModelForm):
    class Meta:
        model = EducationalResume


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication


class InventionForm(forms.ModelForm):
    class Meta:
        model = Invention


class ExecutiveResearchProjectForm(forms.ModelForm):
    class Meta:
        model = ExecutiveResearchProject


class LanguageSkillForm(forms.ModelForm):
    class Meta:
        model = LanguageSkill


class SoftwareSkillForm(forms.ModelForm):
    class Meta:
        model = SoftwareSkill


