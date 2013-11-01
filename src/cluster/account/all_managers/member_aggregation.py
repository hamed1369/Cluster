# -*- coding: utf-8 -*-
import datetime
from django import forms
from cluster.account.account.models import Member, Cluster
from cluster.project.models import Project
from cluster.utils.forms import ClusterBaseModelForm, ClusterFilterModelForm
from cluster.utils.manager.main import ObjectsManager, ManagerColumn, ManagerGroupHeader
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class MemberForm(ClusterFilterModelForm):
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


class MemberAggregationManager(ObjectsManager):
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

    def __init__(self, http_request):
        super(MemberAggregationManager, self).__init__(http_request)

        member_ages = self.get_all_data_cashed()
        print Member.objects.all().count()
        for age_range in member_ages:
            range_members = Member.objects.filter(birth_date__range=(age_range.from_date, age_range.until_date))
            print range_members.count()
            confirmed_members = range_members.filter(is_confirmed=True).distinct().count()
            age_range.confirmed_members = confirmed_members
            unconfirmed_members = range_members.filter(is_confirmed__isnull=True).distinct().count()
            age_range.unconfirmed_members = unconfirmed_members
            not_confirmed_members = range_members.filter(is_confirmed=False).distinct().count()
            age_range.not_confirmed_members = not_confirmed_members

            age_range.project_type_1 += Project.objects.filter(project_status=-1, single_member__birth_date__range=(
                age_range.from_date, age_range.until_date)).distinct().count()
            age_range.project_type0 += Project.objects.filter(project_status=0, single_member__birth_date__range=(
                age_range.from_date, age_range.until_date)).distinct().count()
            age_range.project_type1 += Project.objects.filter(project_status=1, single_member__birth_date__range=(
                age_range.from_date, age_range.until_date)).distinct().count()
            age_range.project_type2 += Project.objects.filter(project_status=2, single_member__birth_date__range=(
                age_range.from_date, age_range.until_date)).distinct().count()
            age_range.project_type3 += Project.objects.filter(project_status=3, single_member__birth_date__range=(
                age_range.from_date, age_range.until_date)).distinct().count()
            age_range.project_type4 += Project.objects.filter(project_status=4, single_member__birth_date__range=(
                age_range.from_date, age_range.until_date)).distinct().count()

            age_range.project_type_1 += Project.objects.filter(project_status=-1, cluster__members__birth_date__range=(
                age_range.from_date, age_range.until_date)).distinct().count()
            age_range.project_type0 += Project.objects.filter(project_status=0, cluster__members__birth_date__range=(
                age_range.from_date, age_range.until_date)).distinct().count()
            age_range.project_type1 += Project.objects.filter(project_status=1, cluster__members__birth_date__range=(
                age_range.from_date, age_range.until_date)).distinct().count()
            age_range.project_type2 += Project.objects.filter(project_status=2, cluster__members__birth_date__range=(
                age_range.from_date, age_range.until_date)).distinct().count()
            age_range.project_type3 += Project.objects.filter(project_status=3, cluster__members__birth_date__range=(
                age_range.from_date, age_range.until_date)).distinct().count()
            age_range.project_type4 += Project.objects.filter(project_status=4, cluster__members__birth_date__range=(
                age_range.from_date, age_range.until_date)).distinct().count()


    def get_all_data(self):
        return [
            MemberAgePeriod(1, 0, 20),
            MemberAgePeriod(2, 20, 30),
            MemberAgePeriod(3, 30, 40),
            MemberAgePeriod(4, 40, 50),
            MemberAgePeriod(5, 50, 100),
        ]

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"رده سنی", '20'),
            ManagerColumn('confirmed_members', u"تاییدشده", '10', aggregation=True),
            ManagerColumn('unconfirmed_members', u"تاییدنشده", '10', aggregation=True),
            ManagerColumn('not_confirmed_members', u"ردشده", '10', aggregation=True),
            ManagerColumn('project_type_1', u"رد شده", '10', aggregation=True),
            ManagerColumn('project_type0', u"در مرحله درخواست", '10', aggregation=True),
            ManagerColumn('project_type1', u"تایید مرحله اول", '10', aggregation=True),
            #ManagerColumn('project_type2', u"تاییدشده توسط داور", '10', aggregation=True),
            ManagerColumn('project_type3', u"تایید مرحله دوم", '10', aggregation=True),
            ManagerColumn('project_type4', u"تکمیل شده", '10', aggregation=True),
        ]
        return columns

    def can_view(self):
        if PermissionController.is_admin(self.http_request.user):
            return True
        return False

    def get_group_headers(self):
        group_headers = [
            ManagerGroupHeader('confirmed_members', 3, u"تعداد اعضا"),
            ManagerGroupHeader('project_type_1', 4, u"تعداد طرح ها"),
        ]
        return group_headers


class MemberAgePeriod(object):
    def __init__(self, age_id, from_age, until_age):
        self.id = age_id
        self.confirmed_members = 0
        self.unconfirmed_members = 0
        self.not_confirmed_members = 0
        self.project_type_1 = 0
        self.project_type0 = 0
        self.project_type1 = 0
        self.project_type2 = 0
        self.project_type3 = 0
        self.project_type4 = 0
        self.from_age = from_age
        self.until_age = until_age

        self.title = unicode(from_age) + ' - ' + unicode(until_age)

        now = datetime.date.today()
        self.until_date = datetime.date(year=now.year - from_age, month=now.month, day=now.day)
        self.from_date = datetime.date(year=now.year - until_age, month=now.month, day=now.day)
