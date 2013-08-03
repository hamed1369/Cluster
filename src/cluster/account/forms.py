# -*- coding:utf-8 -*-
from django import forms

__author__ = 'M.Y'


class SignInForm(forms.Form):
    username = forms.CharField(label=u"نام کاربری",
                               widget=forms.TextInput(
                                   {'placeholder': u'نام کاربری'}))
    password = forms.CharField(label=u"گذرواژه",
                               widget=forms.PasswordInput(
                                   {'placeholder': u'گذرواژه'}))

