# -*- coding: utf-8 -*-
from cluster.account.account.models import Cluster
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.action import ShowAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn

__author__ = 'M.Y'


class ClusterForm(ClusterBaseModelForm):
    class Meta:
        model = Cluster
        fields = ('name', 'domains', 'institute', 'users')


class ClusterActionForm(ClusterBaseModelForm):
    class Meta:
        model = Cluster
        fields = ('name', 'domains', 'institute', 'head', 'users')


class ClusterManager(ObjectsManager):
    manager_name = u"clusters"
    manager_verbose_name = u"مدیریت خوشه ها"
    filter_form = ClusterForm
    actions = [ShowAction(ClusterActionForm)]

    def get_all_data(self):
        return Cluster.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('name', u"نام خوشه", '10'),
            ManagerColumn('domains', u"حوزه فعالیت", '10', True),
            ManagerColumn('institute', u"دانشگاه / موسسه", '10'),
            ManagerColumn('head', u"سر خوشه", '10'),
            ManagerColumn('users', u"اعضا", '10', True),
        ]
        return columns

    def get_domains(self, data):
        return u', '.join([unicode(d) for d in data.domains.filter()])

    def get_users(self, data):
        return u', '.join([unicode(u) for u in data.users.filter()])

