# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from cluster.project.models import Project
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.main import ObjectsManager, ManagerColumn

__author__ = 'M.Y'


class PublicProjectsForMembersFilterForm(ClusterBaseModelForm):
    class Meta:
        model = Project
        fields = ('title', 'keywords', 'domain')


class PublicProjectsForMembersManager(ObjectsManager):
    manager_name = u"projects"
    manager_verbose_name = u"طرح های ثبت و تایید شده"
    filter_form = PublicProjectsForMembersFilterForm

    def get_all_data(self):
        return Project.objects.filter()

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
            </table>
        """
