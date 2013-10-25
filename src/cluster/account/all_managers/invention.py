# -*- coding: utf-8 -*-
from django import forms
from cluster.account.account.models import Cluster
from cluster.account.personal_info.models import Invention
from cluster.utils.forms import ClusterBaseModelForm, ClusterFilterModelForm
from cluster.utils.manager.action import ShowAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class InventionForm(ClusterFilterModelForm):
    class Meta:
        model = Invention
        fields = ('title', 'registration_number', 'registration_date', 'participation')

    def __init__(self, *args, **kwargs):
        super(InventionForm, self).__init__(*args, **kwargs)
        self.fields['cluster'] = forms.ModelChoiceField(queryset=Cluster.objects.filter(), label=u"خوشه مربوطه",
                                                        required=False)


class InventionActionForm(ClusterBaseModelForm):
    class Meta:
        model = Invention
        fields = ('title', 'registration_number', 'registration_date', 'participation')


class ConfirmedInventionManager(ObjectsManager):
    manager_name = u"confirmed_inventions"
    manager_verbose_name = u"مشاهده اختراعات تاییدشده"
    filter_form = InventionForm
    actions = [ShowAction(InventionActionForm)]
    filter_handlers = (
        ('cluster', '', 'cluster_member__cluster'),
        ('title', 'str'),
        ('registration_number', 'this'),
        ('registration_date', 'pdate'),
        ('participation', 'this'),
    )

    def get_all_data(self):
        return Invention.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان اختراع", '30'),
            ManagerColumn('registration_number', u"شماره ثبت", '10'),
            ManagerColumn('registration_date', u"تاریخ ثبت", '10'),
            ManagerColumn('participation', u"شماره ثبت", '10'),
            ManagerColumn('cluster_member', u"عضو خوشه", '10'),
            ManagerColumn('cluster', u"خوشه مربوطه", '10', True),
        ]
        return columns

    def get_cluster(self, data):
        return unicode(data.cluster_member.cluster)

    def can_view(self):
        if PermissionController.is_member(self.http_request.user):
            return True
        return False
