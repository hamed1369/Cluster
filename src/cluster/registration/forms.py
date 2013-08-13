# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from cluster.account.account.models import Member
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from cluster.account.personal_info.models import EducationalResume, Publication, Invention, \
    ExecutiveResearchProject, LanguageSkill, SoftwareSkill
from cluster.project.models import Domain
from cluster.utils.forms import ClusterBaseForm, ClusterBaseModelForm

__author__ = 'M.Y'


class ClusterForm(ClusterBaseForm):
    BOOLEAN_CHOICES = (
        (True, u"بله"),
        (False, u"خیر"),
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
        self.is_cluster_value = is_cluster
        if is_cluster == 'True':
            if not name:
                self._errors['name'] = self.error_class([u"این فیلد برای ایجاد خوشه ضروری است."])
            if not institute:
                self._errors['institute'] = self.error_class([u"این فیلد برای ایجاد خوشه ضروری است."])
        return cd


class RegisterForm(ClusterBaseModelForm):
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
        self.fields.insert(3, 'password', forms.CharField(required=True, label=u"گذرواژه", widget=forms.PasswordInput))
        self.fields.insert(4, 're_password',
                           forms.CharField(required=True, label=u"تکرار گذرواژه", widget=forms.PasswordInput))
        self.fields.insert(5, 'email', forms.EmailField(label=u"پست الکترونیک"))
        self.fields['foundation_of_elites'] = forms.ChoiceField(required=True, choices=RegisterForm.BOOLEAN_CHOICES,
                                                                widget=forms.RadioSelect(), )
        self.fields['foundation_of_elites'].label = u"آیا عضو بنیاد ملی نخبگان می باشید؟"
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs.update({'class': 'validate[required,] text-input'})

    def clean(self):
        cd = super(RegisterForm, self).clean()
        password = cd.get('password')
        re_password = cd.get('re_password')
        if password and re_password and password != re_password:
            self._errors['password'] = self.error_class([u'گذرواژه با تکرار آن مطابقت ندارد.'])
        username = cd.get('username')
        if username:
            users = User.objects.filter(username=username)
            if users:
                self._errors['username'] = self.error_class([u'این نام کاربری تکراری است. لطفا نام دیگری انتخاب کنید.'])

        return cd


class MemberForm(ClusterBaseForm):
    first_name = forms.CharField(label=u"نام")
    last_name = forms.CharField(label=u"نام خانوادگی")
    email = forms.EmailField(label=u"پست الکترونیک")

    def clean(self):
        cd = super(MemberForm, self).clean()
        email = cd.get('email')
        if email:
            users = User.objects.filter(username=email)
            if users:
                self._errors['email'] = self.error_class([u'این ایمیل تکراری است.'])

        return cd


ClusterMemberForm = formset_factory(MemberForm)


class DomainModelForm(ClusterBaseModelForm):
    class Meta:
        model = Domain


ClusterDomainForm = modelformset_factory(Domain, form=DomainModelForm, exclude=('confirmed', ))


class EducationalResumeModelForm(ClusterBaseModelForm):
    class Meta:
        model = EducationalResume


ResumeForm = modelformset_factory(EducationalResume, form=EducationalResumeModelForm, exclude=('cluster_member', ))


class PublicationModelForm(ClusterBaseModelForm):
    class Meta:
        model = Publication


PublicationForm = modelformset_factory(Publication, form=PublicationModelForm, exclude=('cluster_member', ))


class InventionModelForm(ClusterBaseModelForm):
    class Meta:
        model = Invention


InventionForm = modelformset_factory(Invention, form=InventionModelForm, exclude=('cluster_member', ))


class ExecutiveResearchProjectModelForm(ClusterBaseModelForm):
    class Meta:
        model = ExecutiveResearchProject


ExecutiveResearchProjectForm = modelformset_factory(ExecutiveResearchProject, form=ExecutiveResearchProjectModelForm,
                                                    exclude=('cluster_member', ))


class LanguageSkillModelForm(ClusterBaseModelForm):
    class Meta:
        model = LanguageSkill


LanguageSkillForm = modelformset_factory(LanguageSkill, form=LanguageSkillModelForm,
                                         exclude=('cluster_member', ))


class SoftwareSkillModelForm(ClusterBaseModelForm):
    class Meta:
        model = SoftwareSkill


SoftwareSkillForm = modelformset_factory(SoftwareSkill, form=SoftwareSkillModelForm, exclude=('cluster_member', ))
