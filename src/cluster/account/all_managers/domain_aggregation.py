# -*- coding: utf-8 -*-
from django import forms
from cluster.account.account.models import Domain, Cluster, Member
from cluster.project.models import Project
from cluster.utils.forms import ClusterFilterModelForm
from cluster.utils.manager.main import ObjectsManager, ManagerColumn, ManagerGroupHeader
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class DomainForm(ClusterFilterModelForm):
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

    def __init__(self, http_request):
        super(DomainAggregationManager, self).__init__(http_request)

        domains_dict = {}
        domains = self.get_all_data_cashed()
        for domain in domains:
            domains_dict[domain] = {'members_yes': 0, 'members_no': 0, 'members_null': 0, 'clusters_yes': 0,
                                    'clusters_no': 0, 'clusters_null': 0, 'project_type_1': 0, 'project_type0': 0,
                                    'project_type1': 0, 'project_type2': 0, 'project_type3': 0, 'project_type4': 0}

        projects = Project.objects.filter(domain__in=domains).select_related('domain').distinct()
        clusters = Cluster.objects.filter(domains__in=domains).select_related('head', 'domains').distinct()
        members = Member.objects.filter(domain__in=domains).select_related('user', 'domain').distinct()

        for project in projects:
            if project.project_status == -1:
                domains_dict[project.domain]['project_type_1'] += 1
            elif project.project_status == 0:
                domains_dict[project.domain]['project_type0'] += 1
            elif project.project_status == 1:
                domains_dict[project.domain]['project_type1'] += 1
            elif project.project_status == 2:
                domains_dict[project.domain]['project_type2'] += 1
            elif project.project_status == 3:
                domains_dict[project.domain]['project_type3'] += 1
            elif project.project_status == 4:
                domains_dict[project.domain]['project_type4'] += 1

        for cluster in clusters:
            if cluster.head.is_confirmed in [True, 1]:
                for domain in cluster.domains.all():
                    domains_dict[domain]['clusters_yes'] += 1
            elif cluster.head.is_confirmed in [False, 0]:
                for domain in cluster.domains.all():
                    domains_dict[domain]['clusters_no'] += 1
            else:
                for domain in cluster.domains.all():
                    domains_dict[domain]['clusters_null'] += 1

        for member in members:
            if member.is_confirmed is True:
                domains_dict[member.domain]['members_yes'] += 1
            elif member.is_confirmed is False:
                domains_dict[member.domain]['members_no'] += 1
            else:
                domains_dict[member.domain]['members_null'] += 1

        self.domains_dict = domains_dict

    def get_all_data(self):
        return Domain.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('name', u"نام حوزه", '10'),
            ManagerColumn('members_yes', u"تاییدشده", '10', True, aggregation=True),
            ManagerColumn('members_null', u"تاییدنشده", '10', True, aggregation=True),
            ManagerColumn('members_no', u"ردشده", '10', True, aggregation=True),
            ManagerColumn('clusters_yes', u"تاییدشده", '10', True, aggregation=True),
            ManagerColumn('clusters_null', u"تاییدنشده", '10', True, aggregation=True),
            ManagerColumn('clusters_no', u"ردشده", '10', True, aggregation=True),
            ManagerColumn('project_type_1', u"رد شده", '10', True, aggregation=True),
            ManagerColumn('project_type0', u"در مرحله درخواست", '10', True, aggregation=True),
            ManagerColumn('project_type1', u"تایید مرحله اول", '10', True, aggregation=True),
            #ManagerColumn('project_type2', u"تاییدشده توسط داور", '10', True, aggregation=True),
            ManagerColumn('project_type3', u"تایید مرحله دوم", '10', True, aggregation=True),
            ManagerColumn('project_type4', u"تکمیل شده", '10', True, aggregation=True),
        ]
        return columns

    def can_view(self):
        if PermissionController.is_admin(self.http_request.user):
            return True
        return False

    def get_members_yes(self, data):
        return self.domains_dict[data]['members_yes']

    def get_members_null(self, data):
        return self.domains_dict[data]['members_null']

    def get_members_no(self, data):
        return self.domains_dict[data]['members_no']

    def get_clusters_yes(self, data):
        return self.domains_dict[data]['clusters_yes']

    def get_clusters_null(self, data):
        return self.domains_dict[data]['clusters_null']

    def get_clusters_no(self, data):
        return self.domains_dict[data]['clusters_no']

    def get_project_type_1(self, data):
        return self.domains_dict[data]['project_type_1']

    def get_project_type0(self, data):
        return self.domains_dict[data]['project_type0']

    def get_project_type1(self, data):
        return self.domains_dict[data]['project_type1']

    def get_project_type2(self, data):
        return self.domains_dict[data]['project_type2']

    def get_project_type3(self, data):
        return self.domains_dict[data]['project_type3']

    def get_project_type4(self, data):
        return self.domains_dict[data]['project_type4']

    def get_group_headers(self):
        group_headers = [
            ManagerGroupHeader('members_yes', 3, u"تعداد اعضا"),
            ManagerGroupHeader('clusters_yes', 3, u"تعداد خوشه ها"),
            ManagerGroupHeader('project_type_1', 4, u"تعداد طرح ها"),
        ]
        return group_headers
