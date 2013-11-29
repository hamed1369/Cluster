# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
from cluster.account.management.models import IntroPageContent
from cluster.utils.fields import BOOLEAN_CHOICES
from cluster.utils.forms import ClusterBaseModelForm, ClusterBaseForm
from cluster.utils.js_validation import process_js_validations
__author__ = 'M.Y'

class IntroPageForm(ClusterBaseModelForm):

    class Meta:
        model = IntroPageContent

    def __init__(self, *args, **kwargs):
        super(IntroPageForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = TinyMCE(attrs={'cols': 100, 'rows': 20},mce_attrs={
            'content_css': "/static/intro/css/intro.css",
            'force_br_newlines' : False,
            'force_p_newlines' : False,
            'forced_root_block' : '',
            'width': "100%",
            'height': "600",
            'plugins': "fullpage",
            'toolbar': "fullpage",
            'verify_html' : False,
            'cleanup': False
        })

    def save(self, commit=True):
        instance = super(IntroPageForm, self).save(commit)
        IntroPageContent.instance = None
        return instance


class SignInForm(forms.Form):
    username = forms.CharField(label=u"نام کاربری",
                               widget=forms.TextInput(
                                   {'placeholder': u'نام کاربری'}))
    password = forms.CharField(label=u"گذرواژه",
                               widget=forms.PasswordInput(
                                   {'placeholder': u'گذرواژه'}))


class AdminForm(ClusterBaseForm):
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


