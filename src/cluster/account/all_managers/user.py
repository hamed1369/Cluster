# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from tracking.models import Visitor
from cluster.account.actions import ChangeUserName
from cluster.utils.date import handel_date_fields
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.action import AddAction, DeleteAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn
from cluster.utils.permissions import PermissionController
from django import forms

__author__ = 'M.Y'

class UserForm(ClusterBaseModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class UserManager(ObjectsManager):
    manager_name = u"users"
    manager_verbose_name = u"مدیریت کاربران"
    filter_form = UserForm

    actions = [DeleteAction(), ChangeUserName(), AddAction(UserForm)]

    def get_all_data(self):
        return User.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('first_name', u"نام", '10'),
            ManagerColumn('last_name', u"نام خانوادگی", '10'),
            ManagerColumn('username', u"نام کاربری", '10'),
            ]
        return columns

    def can_view(self):
        if PermissionController.is_admin(self.http_request.user):
            return True
        return False

class VisitorForm(ClusterBaseModelForm):
    class Meta:
        model = Visitor
        exclude = ('session_key','ip_address','user_agent','referrer','url','page_views','start_time','last_update')

    def __init__(self, *args, **kwargs):
        super(VisitorForm, self).__init__(*args, **kwargs)
        self.fields['start_time_from'] = forms.DateField(label=u"بازدید از تاریخ", required=False)
        self.fields['start_time_until'] = forms.DateField(label=u"بازدید تا تاریخ", required=False)
        self.fields['first_name'] = forms.CharField(label=u"نام", required=False)
        self.fields['last_name'] = forms.CharField(label=u"نام خانوادگی", required=False)

        handel_date_fields(self)


class VisitorManager(ObjectsManager):
    manager_name = u"visitors"
    manager_verbose_name = u"آمار سایت"
    filter_form = VisitorForm
    actions = [
    ]
    filter_handlers = (
        ('start_time_from', 'pdate', 'start_time__gt'),
        ('start_time_until', 'pdate', 'start_time__lte'),
        ('first_name', 'str', 'user__first_name'),
        ('last_name', 'str', 'user__last_name'),

    )
    def get_all_data(self):
        return Visitor.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('ip_address', u"IP", 5),
            ManagerColumn('user', u"کاربر", 3),
            ManagerColumn('user_agent', u"عامل", 5),
            ManagerColumn('start_time', u"تاریخ بازدید", 3),
            ManagerColumn('session_key', u"کلید نشست", 7),
        ]
        return columns
