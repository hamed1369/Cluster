# -*- coding: utf-8 -*-
from django import forms
from cluster.account.account.models import Member, Cluster
from cluster.account.actions import EditMemberAction
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.action import ShowAction, DeleteAction, ConfirmAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn, ManagerGroupHeader
from cluster.utils.messages import MessageServices
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class MemberForm(ClusterBaseModelForm):
    class Meta:
        model = Member
        fields = ('cluster', 'national_code', 'military_status', 'foundation_of_elites')

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(label=u"نام", required=False)
        self.fields['last_name'] = forms.CharField(label=u"نام خانوادگی", required=False)
        self.fields['cluster'] = forms.ModelMultipleChoiceField(queryset=Cluster.objects.filter(), label=u"خوشه")
        self.fields['foundation_of_elites'] = forms.NullBooleanField(required=False, label=u"عضویت در بنیاد ملی نخبگان")
        self.fields['foundation_of_elites'].widget.choices = ((u'1', u"--- همه ---"),
                                                              (u'2', u"بله"),
                                                              (u'3', u"خیر"))


class MemberManager(ObjectsManager):
    manager_name = u"members_aggregation"
    manager_verbose_name = u"گزارش تجمیعی اعضا"
    filter_form = MemberForm
    filter_handlers = (
        ('first_name', 'str', 'user__first_name'),
        ('last_name', 'str', 'user__last_name'),
        ('cluster', 'm2m'),
        ('national_code', 'this'),
        ('military_status', 'this'),
        ('foundation_of_elites', 'null_bool'),
    )
    aggregation = True
    data_per_page = 30
    height = 500

    def get_all_data(self):
        return [
            MemberAgePeriod(1,'0-20'),
            MemberAgePeriod(2,'20-30'),
            MemberAgePeriod(3,'30-40'),
            MemberAgePeriod(4,'40-50'),
            MemberAgePeriod(5,'50-100'),
                ]

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"رده سنی", '20'),
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


class MemberAgePeriod(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title
