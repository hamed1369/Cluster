# -*- coding: utf-8 -*-
from django import forms
from cluster.account.account.models import Domain
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.action import AddAction, EditAction, DeleteAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class DomainForm(ClusterBaseModelForm):
    class Meta:
        model = Domain
        fields = ('name', 'confirmed')

    def __init__(self, *args, **kwargs):
        super(DomainForm, self).__init__(*args, **kwargs)
        self.fields['confirmed'] = forms.NullBooleanField(required=False, label=u"تایید شده")
        self.fields['confirmed'].widget.choices = ((u'1', u"--- همه ---"),
                                                   (u'2', u"بله"),
                                                   (u'3', u"خیر"))


class DomainManager(ObjectsManager):
    manager_name = u"domains"
    manager_verbose_name = u"مدیریت حوزه ها"
    filter_form = DomainForm
    actions = [AddAction(DomainForm), EditAction(DomainForm, action_verbose_name=u"بررسی و ویرایش"), DeleteAction()]

    def get_all_data(self):
        return Domain.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('name', u"نام حوزه", '10'),
            ManagerColumn('confirmed', u"تایید شده", '10'),
        ]
        return columns

    def can_view(self):
        if PermissionController.is_admin(self.http_request.user):
            return True
        return False
