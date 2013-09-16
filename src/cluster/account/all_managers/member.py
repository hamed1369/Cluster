# -*- coding: utf-8 -*-
from django import forms
from cluster.account.account.models import Member, Cluster
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.action import ShowAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn
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


class MemberActionForm(ClusterBaseModelForm):
    class Meta:
        model = Member

    def __init__(self, *args, **kwargs):
        super(MemberActionForm, self).__init__(*args, **kwargs)
        self.fields['full_name'] = forms.CharField(initial=unicode(self.instance.user), label=u"نام و نام خانوادگی",
                                                   required=False)
        self.fields.keyOrder.remove('full_name')
        self.fields.keyOrder.insert(0, 'full_name')


class MemberManager(ObjectsManager):
    manager_name = u"members"
    manager_verbose_name = u"مدیریت  افراد"
    filter_form = MemberForm
    filter_handlers = (
        ('first_name', 'str'),
        ('last_name', 'str'),
        ('cluster', 'm2m'),
        ('national_code', 'this'),
        ('military_status', 'this'),
        ('foundation_of_elites', 'bool'),
    )
    actions = [ShowAction(MemberActionForm)]

    def get_all_data(self):
        return Member.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('full_name', u"نام و نام خانوادگی", '30', True),
            ManagerColumn('cluster', u"خوشه", '20'),
            ManagerColumn('gender', u"جنسیت", '10'),
            ManagerColumn('national_code', u"کد ملی", '10'),
            ManagerColumn('birth_date', u"تاریخ تولد", '10'),
            ManagerColumn('residence_city', u"شهر محل اقامت", '10'),
            ManagerColumn('mobile', u"تلفن همراه", '10'),
            ManagerColumn('military_status', u"وضعیت نظام وظیفه", '10'),
            ManagerColumn('foundation_of_elites', u"عضویت در بنیاد ملی نخبگان", '10'),
        ]
        return columns

    def get_full_name(self, data):
        return unicode(data.user)

    def can_view(self):
        if PermissionController.is_admin(self.http_request.user):
            return True
        return False


class NoClusterMemberActionForm(ClusterBaseModelForm):
    class Meta:
        model = Member
        fields = ('national_code', 'military_status', 'foundation_of_elites')

    def __init__(self, *args, **kwargs):
        super(NoClusterMemberActionForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(label=u"نام", required=False)
        self.fields['last_name'] = forms.CharField(label=u"نام خانوادگی", required=False)

class NoClusterMemberManager(MemberManager):
    manager_name = u"no_cluster_members"
    manager_verbose_name = u"مدیریت  افراد بدون خوشه"
    filter_form = NoClusterMemberActionForm

    def get_all_data(self):
        return Member.objects.filter(cluster__isnull=True)

