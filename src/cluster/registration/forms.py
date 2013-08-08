# -*- coding:utf-8 -*-
from django import forms
from cluster.account.account.models import Member
from cluster.account.personal_info.models import EducationalResume, Publication, Invention, \
    ExecutiveResearchProject, LanguageSkill, SoftwareSkill

__author__ = 'M.Y'


class ClusterForm(forms.Form):
    BOOLEAN_CHOICES = (
        (1, u"بله"),
        (2, u"خیر"),
    )
    is_cluster = forms.ChoiceField(required=False, choices=BOOLEAN_CHOICES, widget=forms.RadioSelect(),
                                   label=
                                   u"آیا درخواست ثبت خوشه وجود دارد؟(در صورت تایید و ارسال فرم ثبت نام برای اعضاء خوشه)",
    )

    name = forms.CharField(required=False, label=u"نام خوشه (خوشه + حوزه فعالیت + دانشگاه یا موسسه)")

    def __init__(self, *args, **kwargs):
        super(ClusterForm, self).__init__(*args, **kwargs)


class RegisterForm(forms.ModelForm):
    BOOLEAN_CHOICES = (
        (True, u"بله"),
        (False, u"خیر"),
    )

    class Meta:
        model = Member
        exclude = ('cluster', 'user')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields.insert(0, 'first_name', forms.CharField(required=True, label=u"نام"))
        self.fields.insert(1, 'last_name', forms.CharField(required=True, label=u"نام خانوادگی"))
        self.fields.insert(2, 'username', forms.CharField(required=True, label=u"نام کاربری"))
        self.fields.insert(3, 'email', forms.EmailField(label=u"پست الکترونیک"))
        self.fields['foundation_of_elites'] = forms.ChoiceField(required=True, choices=RegisterForm.BOOLEAN_CHOICES,
                                                                widget=forms.RadioSelect(), )
        self.fields['foundation_of_elites'].label = u"آیا عضو بنیاد ملی نخبگان می باشید؟"
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


