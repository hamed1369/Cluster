# -*- coding: utf-8 -*-
from django import forms
from cluster.account.account.models import Domain
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.main import ObjectsManager, ManagerColumn, ManagerGroupHeader
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class DomainForm(ClusterBaseModelForm):
    class Meta:
        model = Domain
        fields = ('name', 'confirmed')

    def __init__(self, *args, **kwargs):
        super(DomainForm, self).__init__(*args, **kwargs)
        self.fields['confirmed'] = forms.NullBooleanField(required=False, label=u"تایید شده", initial=u'2')
        self.fields['confirmed'].widget.choices = ((u'1', u"--- همه ---"),
                                                   (u'2', u"بله"),
                                                   (u'3', u"خیر"))


class DomainAggregationManager(ObjectsManager):
    manager_name = u"domains_aggregation"
    manager_verbose_name = u"گزارش تجمیعی حوزه ها"
    filter_form = DomainForm
    aggregation = True
    data_per_page = 30
    height = 500

    def get_all_data(self):
        return Domain.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('name', u"نام حوزه", '10'),
            ManagerColumn('members', u"تعداد اعضا", '10', True, aggregation=True),
            ManagerColumn('clusters_yes', u"تاییدشده", '10', True, aggregation=True),
            ManagerColumn('clusters_no', u"تاییدنشده", '10', True, aggregation=True),
            ManagerColumn('projects_yes', u"تاییدشده", '10', True, aggregation=True),
            ManagerColumn('projects_no', u"تاییدنشده", '10', True, aggregation=True),
        ]
        return columns

    def can_view(self):
        if PermissionController.is_admin(self.http_request.user):
            return True
        return False

    def get_members(self, data):
        return 2

    def get_clusters_yes(self, data):
        return 2

    def get_clusters_no(self, data):
        return 2

    def get_projects_yes(self, data):
        return 2

    def get_projects_no(self, data):
        return 2

    def get_group_headers(self):
        group_headers = [
            ManagerGroupHeader('clusters_yes', 2, u"تعداد خوشه ها"),
            ManagerGroupHeader('projects_yes', 2, u"تعداد طرح ها"),
        ]
        return group_headers
