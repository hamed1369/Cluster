# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from cluster.account.account.models import Supervisor
from cluster.utils.fields import BOOLEAN_CHOICES
from cluster.utils.forms import ClusterBaseModelForm, ClusterBaseForm
from cluster.utils.js_validation import process_js_validations

__author__ = 'M.Y'


class SignInForm(forms.Form):
    username = forms.CharField(label=u"نام کاربری",
                               widget=forms.TextInput(
                                   {'placeholder': u'نام کاربری'}))
    password = forms.CharField(label=u"گذرواژه",
                               widget=forms.PasswordInput(
                                   {'placeholder': u'گذرواژه'}))


class AdminForm(ClusterBaseModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
        self.fields['change_password'] = forms.ChoiceField(required=False, choices=BOOLEAN_CHOICES,
                                                           widget=forms.RadioSelect(),
                                                           label=u"ویرایش گذرواژه", initial=False)

        self.fields['password'] = forms.CharField(required=False, label=u"گذرواژه جدید", widget=forms.PasswordInput())
        self.fields['re_password'] = forms.CharField(required=False, label=u"تکرار گذرواژه جدید",
                                                     widget=forms.PasswordInput)
        self.extra_js_validation = {
            'username': 'ajax[usernameAjaxEngineCall]',
            're_password': 'equals[id_admin-password]',
        }
        process_js_validations(self)

    def clean(self):
        cd = super(AdminForm, self).clean()
        password = cd.get('password')
        re_password = cd.get('re_password')
        if password and re_password and password != re_password:
            self._errors['password'] = self.error_class([u'گذرواژه با تکرار آن مطابقت ندارد.'])
        return cd

    def save(self, commit=True):
        instance = super(AdminForm, self).save(commit)
        change_pass = self.cleaned_data.get('change_password')
        if change_pass is True or change_pass == 'True':
            password = self.cleaned_data.get('password')
            instance.set_password(password)
            instance.save()
        return instance


class SupervisorForm(ClusterBaseModelForm):
    class Meta:
        model = Supervisor
        fields = ('mobile',)

    def __init__(self, *args, **kwargs):
        super(SupervisorForm, self).__init__(*args, **kwargs)
        self.fields.insert(0, 'first_name', forms.CharField(required=True, label=u"نام"))
        self.fields.insert(1, 'last_name', forms.CharField(required=True, label=u"نام خانوادگی"))
        self.fields.insert(2, 'username', forms.CharField(required=True, label=u"نام کاربری"))
        self.fields.insert(3, 'email', forms.EmailField(label=u"پست الکترونیک"))

        self.fields['password'] = forms.CharField(required=False, label=u"گذرواژه جدید", widget=forms.PasswordInput())
        self.fields['re_password'] = forms.CharField(required=False, label=u"تکرار گذرواژه جدید",
                                                     widget=forms.PasswordInput)
        self.extra_js_validation = {
            'username': 'ajax[usernameAjaxEngineCall]',
            're_password': 'equals[id_password]',
        }
        if self.instance and self.instance.id:
            self.fields.insert(5, 'change_password', forms.ChoiceField(required=False, choices=BOOLEAN_CHOICES,
                                                                       widget=forms.RadioSelect(),
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
            self.fields['password'].is_hidden = True
            self.fields['re_password'].is_hidden = True
            if self.prefix == 'show':
                self.fields['change_password'].is_hidden = True

            if self.http_request.user != self.instance.user:
                del self.extra_js_validation['username']
        process_js_validations(self)

    def clean(self):
        cd = super(SupervisorForm, self).clean()
        password = cd.get('password')
        re_password = cd.get('re_password')
        if password and re_password and password != re_password:
            self._errors['password'] = self.error_class([u'گذرواژه با تکرار آن مطابقت ندارد.'])
        return cd

    def save(self, commit=False):
        instance = super(SupervisorForm, self).save(commit)
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        change_pass = self.cleaned_data.get('change_password')
        password = self.cleaned_data.get('password')
        if not self.instance.id:
            user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email)
            user.set_password(password)
            instance.user = user
        else:
            user = instance.user
        if change_pass is True or change_pass == 'True':
            user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()
        instance.save()
        return instance


class ArbiterInvitationForm(ClusterBaseForm):
    title = forms.CharField(label=u"عنوان")
    email = forms.EmailField(label=u"پست الکترونیکی")
    message = forms.CharField(label=u"پیام", widget=forms.Textarea)
