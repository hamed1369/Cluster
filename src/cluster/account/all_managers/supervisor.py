# -*- coding: utf-8 -*-
from django import forms
from cluster.account.account.models import Supervisor
from cluster.account.forms import SupervisorForm
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.action import DeleteAction, AddAction, EditAction, ShowAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class SupervisorFilterForm(ClusterBaseModelForm):
    class Meta:
        model = Supervisor
        fields = ('mobile',)

    def __init__(self, *args, **kwargs):
        super(SupervisorFilterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(label=u"نام", required=False)
        self.fields['last_name'] = forms.CharField(label=u"نام خانوادگی", required=False)


class SupervisorManager(ObjectsManager):
    manager_name = u"supervisors_management"
    manager_verbose_name = u"ناظران"
    filter_form = SupervisorFilterForm

    actions = [AddAction(SupervisorForm), EditAction(SupervisorForm),
               ShowAction(SupervisorForm), DeleteAction()]

    def get_all_data(self):
        return Supervisor.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('full_name', u"نام و نام خانوادگی", '30', True),
            ManagerColumn('email', u"پست الکترونیک", '10', True),
            ManagerColumn('username', u"نام کاربری", '10', True),
            ManagerColumn('mobile', u"تلفن همراه", '10'),
        ]
        return columns

    def get_full_name(self, data):
        return unicode(data)

    def get_email(self, data):
        return unicode(data.user.email)

    def get_username(self, data):
        return unicode(data.user.username)

    def can_view(self):
        if PermissionController.is_admin(self.http_request.user):
            return True
        return False
