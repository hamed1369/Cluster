# -*- coding: utf-8 -*-
from cluster.project.models import Domain
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.action import AddAction, EditAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class DomainForm(ClusterBaseModelForm):
    class Meta:
        model = Domain
        fields = ('name', 'confirmed')


class DomainManager(ObjectsManager):
    manager_name = u"domains"
    manager_verbose_name = u"مدیریت حوزه ها"
    filter_form = DomainForm
    actions = [AddAction(DomainForm), EditAction(DomainForm)]

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
