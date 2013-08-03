# -*- coding:utf-8 -*-
from django import forms

__author__ = 'M.Y'


class SignInForm(forms.Form):
    username = forms.CharField(label=u"نام کاربری",
                               widget=forms.TextInput({'class': 'form-control  input-large', 'placeholder': u'نام کاربری'}))
    password = forms.CharField(label=u"گذرواژه",
                               widget=forms.PasswordInput({'class': 'form-control  input-large', 'placeholder': u'گذرواژه'}))
