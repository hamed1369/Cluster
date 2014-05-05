# -*- coding: utf-8 -*-
from captcha.fields import CaptchaField
from django import forms
from cluster.account.account.models import Domain, InternationalAccount
from cluster.utils.forms import ClusterBaseModelForm, ClusterFilterModelForm
from cluster.utils.manager.action import AddAction, EditAction, DeleteAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn
from cluster.utils.permissions import PermissionController
import re

__author__ = 'M.Y'


class InternationalAccountRegisterForm(ClusterBaseModelForm):
    my_default_errors = {
        'required': 'This field is required',
        'invalid': 'Enter a valid value'
    }
    captcha = CaptchaField(label=u"security code", error_messages={'invalid': u"security code is not valid"})

    class Meta:
        model = InternationalAccount
        exclude = ('created_on',)

    def __init__(self,*arg, **kwargs):
        super(InternationalAccountRegisterForm,self).__init__(*arg,**kwargs)

        for field in self.fields.iterkeys():
            self.fields[field].error_messages = self.my_default_errors

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if re.findall("[A-Za-z]",mobile):
            self._errors['mobile'] = self.error_class(["Only numbers are acceptable."])
        return mobile

    def clean_telephone(self):
        phone = self.cleaned_data.get('telephone')
        if re.findall("[A-Za-z]",phone):
            self._errors['telephone'] = self.error_class(["Only numbers are acceptable."])
        return phone

class InternationlAccountFilterForm(ClusterFilterModelForm):
    class Meta:
        model = InternationalAccount
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(InternationlAccountFilterForm, self).__init__(*args, **kwargs)

class InternationlAccountManager(ObjectsManager):
    manager_name = u"international_registrations"
    manager_verbose_name = u"مدیریت ثبت نام های بین المللی"
    filter_form = InternationlAccountFilterForm
    #actions = [AddAction(DomainActionForm), EditAction(DomainActionForm, action_verbose_name=u"بررسی و ویرایش"),
    #           DeleteAction()]

    def get_all_data(self):
        return InternationalAccount.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('first_name', u"first name", '10'),
            ManagerColumn('last_name', u"last name", '10'),
            ManagerColumn('email', u"email", '10'),
            ManagerColumn('created_on', u"registration date", '10'),

        ]
        return columns

    def can_view(self):
        if PermissionController.is_admin(self.http_request.user):
            return True
        return False
