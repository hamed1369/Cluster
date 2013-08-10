# -*- coding:utf-8 -*-
from django import forms
from cluster.account.account.models import Member
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from cluster.account.personal_info.models import EducationalResume, Publication, Invention, \
    ExecutiveResearchProject, LanguageSkill, SoftwareSkill
from cluster.project.models import Domain

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

    name = forms.CharField(required=False, label=u"نام خوشه")
    institute = forms.CharField(required=False, label=u"دانشگاه / موسسه", max_length=30)

    def __init__(self, *args, **kwargs):
        super(ClusterForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = super(ClusterForm, self).clean()
        is_cluster = cd.get('is_cluster')
        name = cd.get('name')
        institute = cd.get('institute')
        if is_cluster == 1:
            if not name:
                self._errors['name'] = self.error_class([u"این فیلد برای ایجاد خوشه ضروری است."])
            if not institute:
                self._errors['institute'] = self.error_class([u"این فیلد برای ایجاد خوشه ضروری است."])
        return cd


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
    first_name = forms.CharField(label=u"نام")
    last_name = forms.CharField(label=u"نام خانوادگی")
    email = forms.EmailField(label=u"پست الکترونیک")


CLusterMemberForm = formset_factory(MemberForm)
ClusterDomainForm = modelformset_factory(Domain, exclude=('confirmed', ))

ResumeForm = modelformset_factory(EducationalResume, exclude=('cluster_member', ))
PublicationForm = modelformset_factory(Publication, exclude=('cluster_member', ))
InventionForm = modelformset_factory(Invention, exclude=('cluster_member', ))
ExecutiveResearchProjectForm = modelformset_factory(ExecutiveResearchProject, exclude=('cluster_member', ))
LanguageSkillForm = modelformset_factory(LanguageSkill, exclude=('cluster_member', ))
SoftwareSkillForm = modelformset_factory(SoftwareSkill, exclude=('cluster_member', ))
