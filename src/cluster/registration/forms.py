# -*- coding:utf-8 -*-
from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.models import User
from cluster.account.account.models import Member, Arbiter
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from cluster.account.personal_info.models import EducationalResume, Publication, Invention, \
    ExecutiveResearchProject, LanguageSkill, SoftwareSkill
from cluster.project.models import Domain
from cluster.utils.fields import BOOLEAN_CHOICES
from cluster.utils.forms import ClusterBaseForm, ClusterBaseModelForm
from cluster.utils.js_validation import process_js_validations

__author__ = 'M.Y'


class ClusterForm(ClusterBaseForm):
    is_cluster = forms.ChoiceField(choices=BOOLEAN_CHOICES, widget=forms.RadioSelect(),
                                   label=u"ثبت نام به صورت خوشه ای",required=True,initial=False
    )

    name = forms.CharField(required=False, label=u"نام خوشه")
    institute = forms.CharField(required=False, label=u"دانشگاه / موسسه", max_length=30)

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
        self.fields['foundation_of_elites'] = forms.ChoiceField(required=True, choices=BOOLEAN_CHOICES,
                                                                widget=forms.RadioSelect(), )
        self.fields['foundation_of_elites'].label = u"آیا عضو بنیاد ملی نخبگان می باشید؟"

        self.fields.insert(len(self.fields), 'captcha', CaptchaField(label=u"کد امنیتی", error_messages={
            'invalid': u"کد امنیتی وارد شده صحیح نمی باشد."}))

        if self.instance and self.instance.id:
            self.fields.insert(3, 'change_password',
                               forms.ChoiceField(required=False, choices=BOOLEAN_CHOICES, widget=forms.RadioSelect(),
                                                 label=u"ویرایش گذرواژه", initial=False))
            self.fields['password'].label = u"گذرواژه جدید"
            self.fields['password'].required = False
            self.fields['re_password'].label = u"تکرار گذرواژه جدید"
            self.fields['re_password'].required = False
            if self.instance.user:
                self.fields['first_name'].initial = self.instance.user.first_name
                self.fields['last_name'].initial = self.instance.user.last_name
                self.fields['username'].initial = self.instance.user.username
                self.fields['email'].initial = self.instance.user.email
            self.extra_js_validation = {
                'username': 'ajax[usernameAjaxEngineCall]',
                'essential_telephone': 'custom[phone]',
                'mobile': 'custom[mobile]',
            }
        else:
            self.extra_js_validation = {
                're_password': 'equals[id_register-password]',
                'username': 'ajax[usernameAjaxEngineCall]',
                'email': 'ajax[emailAjaxEngineCall]',
                'essential_telephone': 'custom[phone]',
                'mobile': 'custom[mobile]',
            }

        process_js_validations(self)

    def clean(self):
        cd = super(RegisterForm, self).clean()
        password = cd.get('password')
        re_password = cd.get('re_password')
        if password and re_password and password != re_password:
            self._errors['password'] = self.error_class([u'گذرواژه با تکرار آن مطابقت ندارد.'])
        username = cd.get('username')
        if username:
            users = User.objects.filter(username=username)
            if self.instance.id:
                users = users.exclude(id=self.instance.user.id)
            if users:
                self._errors['username'] = self.error_class([u'این نام کاربری تکراری است. لطفا نام دیگری انتخاب کنید.'])

        return cd

    def save(self, commit=True, user=None):
        member = super(RegisterForm, self).save(commit)
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        change_pass = self.cleaned_data.get('change_password')

        try:
            if not user:
                user = member.user
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            if change_pass is True or change_pass == 'True':
                user.set_password(password)
            member.user = user
        except User.DoesNotExist:
            user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, )
            user.set_password(password)
            member.user = user
        user.save()
        return member


class MemberForm(ClusterBaseForm):
    first_name = forms.CharField(label=u"نام")
    last_name = forms.CharField(label=u"نام خانوادگی")
    email = forms.EmailField(label=u"پست الکترونیک", widget=forms.TextInput(attrs={'style': 'width:85%;'}))
    domain = forms.CharField(label=u"حوزه فعالیت", widget=forms.Select(choices=[(u'', '---------'), ]))

    extra_js_validation = {
        'email': 'ajax[emailAjaxEngineCall]',
    }

    def clean(self):
        cd = super(MemberForm, self).clean()
        user_domain_id = None
        if 'user_domain_id' in self.fields:
            user_domain_id = self.fields['user_domain_id'].initial
            cd['user_domain_id'] = self.fields['user_domain_id'].initial
        email = cd.get('email')
        if email:
            users = User.objects.filter(username=email)
            if user_domain_id:
                users = users.exclude(user_domain__id=user_domain_id)
            if users:
                self._errors['email'] = self.error_class([u'این ایمیل تکراری است.'])
        return cd

    def init_by_user_domain(self, user_domain, is_head):
        self.fields['first_name'].initial = user_domain.user.first_name
        self.fields['last_name'].initial = user_domain.user.last_name
        self.fields['email'].initial = user_domain.user.email
        self.fields['domain'].initial = user_domain.domain.id

        choices = [(u'', '---------'), ]
        for domain in user_domain.clusters.all()[0].domains.all():
            choices.append((unicode(domain.id), domain.name))

        self.fields['domain'].widget = forms.Select(choices=choices)
        if not is_head:
            self.fields['first_name'].widget.attrs.update({'readonly': 'readonly'})
            self.fields['last_name'].widget.attrs.update({'readonly': 'readonly'})
            self.fields['email'].widget.attrs.update({'readonly': 'readonly'})
            self.fields['domain'].widget.attrs.update({'readonly': 'readonly'})
        self.fields.insert(0, 'user_domain_id', forms.CharField(widget=forms.HiddenInput(), initial=user_domain.id))
        self.extra_js_validation.clear()
        process_js_validations(self)


ClusterMemberForm = formset_factory(MemberForm, can_delete=True)


class DomainForm(ClusterBaseForm):
    domain_choice = forms.ModelChoiceField(queryset=Domain.objects.filter(confirmed=True), label=u"نام حوزه",
                                           required=False, empty_label=u"سایر")
    new_domain_name_widget = forms.TextInput(attrs={"style": 'display:none;'})
    new_domain_name_widget.is_hidden = True
    new_domain_name = forms.CharField(label=u"نام حوزه", max_length=40,
                                      widget=new_domain_name_widget, required=False)

    def init_by_domain(self, domain, is_head):
        if is_head:
            if domain.confirmed:
                self.fields['domain_choice'].initial = domain
            else:
                self.fields['new_domain_name'].initial = domain.name
        else:
            self.fields['domain_choice'] = forms.CharField(label=u"نام حوزه")
            self.fields['domain_choice'].initial = domain.name
            self.fields['domain_choice'].widget.attrs.update({'readonly': 'readonly'})


ClusterDomainForm = formset_factory(DomainForm, can_delete=True)


class EducationalResumeModelForm(ClusterBaseModelForm):
    js_validation_configs = {
        'required': False,
    }

    class Meta:
        model = EducationalResume


ResumeForm = modelformset_factory(EducationalResume, form=EducationalResumeModelForm, exclude=('cluster_member', ),
                                  can_delete=True)


class PublicationModelForm(ClusterBaseModelForm):
    js_validation_configs = {
        'required': False,
    }

    class Meta:
        model = Publication


PublicationForm = modelformset_factory(Publication, form=PublicationModelForm, exclude=('cluster_member', ),
                                       can_delete=True)


class InventionModelForm(ClusterBaseModelForm):
    js_validation_configs = {
        'required': False,
    }

    class Meta:
        model = Invention


InventionForm = modelformset_factory(Invention, form=InventionModelForm, exclude=('cluster_member', ), can_delete=True)


class ExecutiveResearchProjectModelForm(ClusterBaseModelForm):
    js_validation_configs = {
        'required': False,
    }

    class Meta:
        model = ExecutiveResearchProject


ExecutiveResearchProjectForm = modelformset_factory(ExecutiveResearchProject, form=ExecutiveResearchProjectModelForm,
                                                    exclude=('cluster_member', ), can_delete=True)


class LanguageSkillModelForm(ClusterBaseModelForm):
    js_validation_configs = {
        'required': False,
    }

    class Meta:
        model = LanguageSkill


LanguageSkillForm = modelformset_factory(LanguageSkill, form=LanguageSkillModelForm,
                                         exclude=('cluster_member', ), can_delete=True)


class SoftwareSkillModelForm(ClusterBaseModelForm):
    js_validation_configs = {
        'required': False,
    }

    class Meta:
        model = SoftwareSkill


SoftwareSkillForm = modelformset_factory(SoftwareSkill, form=SoftwareSkillModelForm, exclude=('cluster_member', ),
                                         can_delete=True)


class ArbiterForm(ClusterBaseModelForm):
    class Meta:
        model = Arbiter
        exclude = ('user', 'is_confirmed')

    extra_js_validation = {
        're_password': 'equals[id_register-password]',
        'username': 'ajax[usernameAjaxEngineCall]',
        'email': 'ajax[emailAjaxEngineCall]',
        'essential_telephone': 'custom[phone]',
        'mobile': 'custom[mobile]',
        'office_phone': 'custom[phone]',
        'fax': 'custom[phone]',
    }

    def __init__(self, *args, **kwargs):
        super(ArbiterForm, self).__init__(*args, **kwargs)
        self.fields.insert(0, 'first_name', forms.CharField(required=True, label=u"نام"))
        self.fields.insert(1, 'last_name', forms.CharField(required=True, label=u"نام خانوادگی"))
        self.fields.insert(2, 'username', forms.CharField(required=True, label=u"نام کاربری"))
        self.fields.insert(3, 'password', forms.CharField(required=True, label=u"گذرواژه", widget=forms.PasswordInput))
        self.fields.insert(4, 're_password',
                           forms.CharField(required=True, label=u"تکرار گذرواژه", widget=forms.PasswordInput))
        self.fields.insert(5, 'email', forms.EmailField(label=u"پست الکترونیک"))
        if self.instance and self.instance.id:
            self.fields.insert(3, 'change_password',
                               forms.ChoiceField(required=False, choices=BOOLEAN_CHOICES, widget=forms.RadioSelect(),
                                                 label=u"ویرایش گذرواژه", initial=False))
            self.fields['password'].label = u"گذرواژه جدید"
            self.fields['password'].required = False
            self.fields['re_password'].label = u"تکرار گذرواژه جدید"
            self.fields['re_password'].required = False
            if self.instance.user:
                self.fields['first_name'].initial = self.instance.user.first_name
                self.fields['last_name'].initial = self.instance.user.last_name
                self.fields['username'].initial = self.instance.user.username
                self.fields['username'].widget.attrs.update('readonly', 'readonly')
                self.fields['email'].initial = self.instance.user.email

        self.fields['interested_domain'].queryset = Domain.objects.filter(confirmed=True)
        self.fields['interested_domain'].widget = forms.CheckboxSelectMultiple()
        self.fields['interested_domain'].label = u"حوزه های مورد علاقه برای داوری"
        process_js_validations(self)

    def save(self, commit=True):
        instance = super(ArbiterForm, self).save(commit=False)
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        change_pass = self.cleaned_data.get('change_password')
        try:
            user = instance.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            if change_pass is True or change_pass == 'True':
                user.set_password(password)
        except Exception:
            user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, )
            user.set_password(password)

        user.save()
        instance.user = user
        instance.save()

        instance.interested_domain = self.cleaned_data.get('interested_domain')

        return instance

