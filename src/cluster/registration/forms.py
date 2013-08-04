# -*- coding:utf-8 -*-
from django import forms
from cluster.account.account.models import Member
from cluster.account.personal_info.models import EducationalResume, Publication, Invention, \
    ExecutiveResearchProject, LanguageSkill, SoftwareSkill

__author__ = 'M.Y'


class RegisterForm(forms.ModelForm):
    is_cluster = forms.BooleanField(required=False,
                                    label=
                                    u"آیا درخواست ثبت خوشه وجود دارد؟(در صورت تایید و ارسال فرم ثبت نام برای اعضاء خوشه)", )

    class Meta:
        model = Member

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member


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


