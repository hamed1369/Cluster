# -*- coding: utf-8 -*-
from django import forms
from django.db.models.query_utils import Q
from cluster.account.account.models import Cluster, Member, Domain
from cluster.project.forms import ProjectManagerForm
from cluster.project.models import Project
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.action import EditAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class PublicProjectsForMembersFilterForm(ClusterBaseModelForm):
    class Meta:
        model = Project
        fields = ('title', 'keywords', 'domain')


class PublicProjectsForMembersManager(ObjectsManager):
    manager_name = u"projects"
    manager_verbose_name = u"طرح های من"
    filter_form = PublicProjectsForMembersFilterForm

    def can_view(self):
        if PermissionController.is_member(self.http_request.user):
            return True

    def get_all_data(self):
        return Project.objects.filter(Q(single_member=self.http_request.user.member)|Q(cluster__user_domains__user=self.http_request.user))

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", '10'),
            ManagerColumn('keywords', u"کلید واژه ها", '10'),
            ManagerColumn('domain', u"حوزه طرح", '10'),
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


class ProjectsForArbitersFilterForm(ClusterBaseModelForm):
    class Meta:
        model = Project
        fields = ('title', 'keywords', 'domain', 'project_status', 'cluster', 'single_member')

    def __init__(self, *args, **kwargs):
        super(ProjectsForArbitersFilterForm, self).__init__(*args, **kwargs)
        self.fields['cluster'] = forms.ModelMultipleChoiceField(queryset=Cluster.objects.filter(), label=u"خوشه مربوطه",
                                                                required=False)
        self.fields['domain'] = forms.ModelMultipleChoiceField(queryset=Domain.objects.filter(), label=u"دامنه ها",
                                                               required=False)
        self.fields['single_member'] = forms.ModelMultipleChoiceField(queryset=Member.objects.filter(), label=u"اعضا",
                                                                      required=False)


class ProjectsManagement(ObjectsManager):
    manager_name = u"projects_management"
    manager_verbose_name = u"مدیریت طرح ها"
    filter_form = ProjectsForArbitersFilterForm
    actions = [EditAction(ProjectManagerForm, action_verbose_name=u"بررسی", form_title=u"بررسی طرح")]

    filter_handlers = (
        ('title', 'str'),
        ('keywords', 'str'),
        ('domain', 'm2m'),
        ('project_status', ''),
        ('cluster', 'm2m'),
        ('single_member', 'm2m'),
    )

    def can_view(self):
        if PermissionController.is_admin(self.http_request.user) or PermissionController.is_arbiter(
                self.http_request.user):
            return True
        return False

    def get_all_data(self):
        return Project.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", '10'),
            ManagerColumn('keywords', u"کلید واژه ها", '10'),
            ManagerColumn('domain', u"حوزه طرح", '10'),
            ManagerColumn('project_status', u"مرحله داوری", '10'),
        ]
        return columns
