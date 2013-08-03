# -*- coding:utf-8 -*-
from django import forms
from cluster.account.account.models import Account

__author__ = 'M.Y'


class RegisterForm(forms.ModelForm):
    is_cluster = forms.BooleanField(required=False,
                                    label=u"آیا درخواست ثبت خوشه وجود دارد؟(در صورت تایید و ارسال فرم ثبت نام برای اعضاء خوشه)")

    class Meta:
        model = Account

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

