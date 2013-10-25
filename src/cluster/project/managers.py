# -*- coding: utf-8 -*-
from django import forms
from django.db.models.query_utils import Q
from cluster.account.account.models import Cluster, Member, Domain
from cluster.project.actions import ProjectDetailAction, ProjectDetailMemberAction, EditProjectAction, AdminProjectCheckAction, ArbiterProjectCheckAction
from cluster.project.models import Project
from cluster.utils.date import handel_date_fields
from cluster.utils.forms import ClusterBaseModelForm, ClusterFilterModelForm
from cluster.utils.manager.action import DeleteAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class MemberProjectFilterForm(ClusterFilterModelForm):
    class Meta:
        model = Project
        fields = ('title', 'keywords', 'domain')


class MemberProjectManager(ObjectsManager):
    manager_name = u"projects"
    manager_verbose_name = u"طرح های من"
    filter_form = MemberProjectFilterForm

    actions = [EditProjectAction(), DeleteAction(action_verbose_name=u"انصراف از طرح"), ProjectDetailMemberAction()]

    def can_view(self):
        if PermissionController.is_member(self.http_request.user):
            return True

    def get_all_data(self):
        return Project.objects.filter(
            Q(single_member=self.http_request.user.member) | Q(cluster__members__user=self.http_request.user))

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", '10'),
            ManagerColumn('keywords', u"کلید واژه ها", '10'),
            ManagerColumn('domain', u"حوزه طرح", '10'),
            ManagerColumn('state', u"مرحله", '10'),
            ManagerColumn('project_status', u"مرحله داوری", '10'),
        ]
        return columns

    def get_filter_form_content(self):
        return """
            <table style="width:100%">
                <tr>
                    <td width="10%">{{ form.title.label }}</td>
                    <td width="20%">{{ form.title }}</td>
                    <td width="20%">{{ form.domain.label }}</td>
                    <td width="20%">{{ form.domain }}</td>
                    <td width="10%">{{ form.keywords.label }}</td>
                    <td width="20%">{{ form.keywords }}</td>
                </tr>
                <tr>
                    <td colspan="10" style="text-align: left;">
                        <input type="reset" value="بازنشانی" class="filter-reset">
                        <input type="submit" value="جستجو" class="filter-submit">
                    </td>
                </tr>
            </table>
        """


class ProjectsManagementFilterForm(ClusterFilterModelForm):
    class Meta:
        model = Project
        fields = ('title', 'keywords', 'domain', 'project_status', 'cluster', 'single_member')

    def __init__(self, *args, **kwargs):
        super(ProjectsManagementFilterForm, self).__init__(*args, **kwargs)
        self.fields['cluster'] = forms.ModelMultipleChoiceField(queryset=Cluster.objects.filter(), label=u"خوشه مربوطه",
                                                                required=False)
        self.fields['domain'] = forms.ModelMultipleChoiceField(queryset=Domain.objects.filter(), label=u"دامنه ها",
                                                               required=False)
        self.fields['single_member'] = forms.ModelMultipleChoiceField(queryset=Member.objects.filter(), label=u"اعضا",
                                                                      required=False)
        self.fields['project_status'].choices = (
            ('', u"---همه---"),
            (-1, u"رد شده"),
            (0, u"در مرحله درخواست"),
            (1, u"تایید مرحله اول"),
            (2, u"تایید مرحله دوم"),
            (4, u"تکمیل شده"),
        )
        self.fields['milestone_from'] = forms.DateField(label=u"موعدها از تاریخ", required=False)
        self.fields['milestone_until'] = forms.DateField(label=u"موعدها تا تاریخ", required=False)
        handel_date_fields(self)


class ProjectsManagement(ObjectsManager):
    manager_name = u"projects_management"
    manager_verbose_name = u"مدیریت طرح ها"
    filter_form = ProjectsManagementFilterForm
    actions = [AdminProjectCheckAction(), ProjectDetailAction()]

    filter_handlers = (
        ('title', 'str'),
        ('keywords', 'str'),
        ('domain', 'm2m'),
        ('project_status', ''),
        ('cluster', 'm2m'),
        ('single_member', 'm2m'),
        ('milestone_from', 'pdate', 'milestones__milestone_date__gte'),
        ('milestone_until', 'pdate', 'milestones__milestone_date__lte'),
    )

    def can_view(self):
        if PermissionController.is_admin(self.http_request.user):
            return True
        return False

    def get_all_data(self):
        return Project.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", '10'),
            ManagerColumn('cluster', u"خوشه", '10', True, True),
            ManagerColumn('keywords', u"کلید واژه ها", '10'),
            ManagerColumn('domain', u"حوزه طرح", '10'),
            ManagerColumn('state', u"مرحله", '10'),
            ManagerColumn('project_status', u"مرحله داوری", '10'),
        ]
        return columns

    def get_cluster(self, data):
        if data.cluster:
            link = u"/clusters/actions/?t=action&n=edit_cluster&i=%s" % data.cluster.id
            return u"""<a onClick="MyWindow=window.open('%s','خوشه/فرد',width=800,height=600); return false;"href='#' class="jqgrid-a">%s</a>""" % (
                link, unicode(data.cluster))
        if data.single_member and not data.cluster:
            link = u"/members/actions/?t=action&n=edit_member&i=%s" % data.single_member.id
            return u"""<a onClick="MyWindow=window.open('%s','خوشه/فرد',width=800,height=600); return false;"href='#' class="jqgrid-a">%s</a>""" % (
                link, unicode(data.single_member))


class ArbiterProjectsFilterForm(ClusterFilterModelForm):
    class Meta:
        model = Project
        fields = ('title', 'keywords', 'domain', 'cluster', 'single_member')

    def __init__(self, *args, **kwargs):
        super(ArbiterProjectsFilterForm, self).__init__(*args, **kwargs)
        self.fields['cluster'] = forms.ModelMultipleChoiceField(queryset=Cluster.objects.filter(), label=u"خوشه مربوطه",
                                                                required=False)
        self.fields['domain'] = forms.ModelMultipleChoiceField(queryset=Domain.objects.filter(), label=u"دامنه ها",
                                                               required=False)
        self.fields['single_member'] = forms.ModelMultipleChoiceField(queryset=Member.objects.filter(), label=u"اعضا",
                                                                      required=False)
        self.fields['milestone_from'] = forms.DateField(label=u"موعدها از تاریخ", required=False)
        self.fields['milestone_until'] = forms.DateField(label=u"موعدها تا تاریخ", required=False)
        handel_date_fields(self)


class ArbiterProjectsManagement(ProjectsManagement):
    manager_name = u"projects_arbitration"
    manager_verbose_name = u"مدیریت طرح ها"
    filter_form = ArbiterProjectsFilterForm
    actions = [ArbiterProjectCheckAction(), ProjectDetailAction()]

    def can_view(self):
        if PermissionController.is_arbiter(self.http_request.user):
            return True
        return False

    def get_all_data(self):
        return Project.objects.filter(project_arbiters__arbiter=self.http_request.user.arbiter,
                                      project_arbiters__project__project_status=Project.MIDDLE_CONFIRM_STATE)

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", '10'),
            ManagerColumn('cluster', u"خوشه", '10', True),
            ManagerColumn('keywords', u"کلید واژه ها", '10'),
            ManagerColumn('domain', u"حوزه طرح", '10'),
            ManagerColumn('state', u"مرحله", '10'),
            ManagerColumn('project_status', u"مرحله داوری", '10'),
        ]
        return columns

    def get_cluster(self, data):
        if data.cluster:
            return unicode(data.cluster)
        if data.single_member and not data.cluster:
            return unicode(data.single_member)


class SupervisorProjectsManagement(ArbiterProjectsManagement):
    manager_name = u"projects_supervision"
    manager_verbose_name = u"مدیریت طرح ها"
    filter_form = ArbiterProjectsFilterForm
    actions = [ProjectDetailAction(has_comments=False)]

    def can_view(self):
        if PermissionController.is_supervisor(self.http_request.user):
            return True
        return False

    def get_all_data(self):
        return Project.objects.filter(supervisor=self.http_request.user.supervisor)
