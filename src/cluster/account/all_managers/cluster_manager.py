# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from cluster.account.account.models import Cluster
from cluster.account.actions import ClusterConfirmAction, EditClusterAction
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.action import ShowAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class ClusterForm(ClusterBaseModelForm):
    class Meta:
        model = Cluster
        fields = ('name', 'domains', 'institute', 'degree')

    def __init__(self, *args, **kwargs):
        super(ClusterForm, self).__init__(*args, **kwargs)
        self.fields['users'] = forms.ModelMultipleChoiceField(queryset=User.objects.filter(), label=u"اعضا",
                                                              required=False)
        self.fields['confirmed'] = forms.NullBooleanField(required=False, label=u"تایید شده")
        self.fields['confirmed'].widget.choices = ((u'1', u"--- همه ---"),
                                                   (u'2', u"بله"),
                                                   (u'3', u"خیر"))


class ClusterActionForm(ClusterBaseModelForm):
    class Meta:
        model = Cluster
        fields = ('name', 'domains', 'institute', 'head', 'degree')

    def __init__(self, *args, **kwargs):
        super(ClusterActionForm, self).__init__(*args, **kwargs)
        self.fields['users'] = forms.ModelMultipleChoiceField(queryset=User.objects.filter(), label=u"اعضا",
                                                              required=False)
        self.fields['users'].initial = self.instance.user_domains.all().values_list('user', flat=True)


class ClusterManager(ObjectsManager):
    manager_name = u"clusters"
    manager_verbose_name = u"مدیریت خوشه ها"
    filter_form = ClusterForm
    actions = [ShowAction(ClusterActionForm, height='300'), EditClusterAction(), ClusterConfirmAction()]

    filter_handlers = (
        ('name', 'str'),
        ('domains', 'm2m'),
        ('institute', 'str'),
        ('head', 'm2o'),
        ('users', '', 'user_domains__user__in'),
        ('confirmed', 'null_bool', 'head__is_confirmed'),
    )

    def get_all_data(self):
        return Cluster.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('name', u"نام خوشه", '10'),
            ManagerColumn('domains', u"حوزه فعالیت", '10', True),
            ManagerColumn('institute', u"دانشگاه / موسسه", '10'),
            ManagerColumn('head', u"سر خوشه", '10'),
            ManagerColumn('users', u"اعضا", '11', True, True),
            ManagerColumn('created_on', u"تاریخ ثبت", '10'),
            ManagerColumn('confirm', u"تاییدشده", '10', True),
            ManagerColumn('degree', u"درجه", '10'),
        ]
        return columns

    def get_domains(self, data):
        return u', '.join([unicode(d) for d in data.domains.filter()])

    def get_users(self, data):
        res = u"""<ol>"""
        for item in data.get_members_and_links():
            if item[1]:
                res += u"""<li><a onClick="MyWindow=window.open('%s','جزئیات عضو',width=800,height=600); return false;"href='#' class="jqgrid-a">%s</a></li>""" % (
                    item[1], item[0])
            else:
                res += u"""<li>%s (عدم ثبت نام)</li>""" % (item[0])

        res += u"""</ol>"""
        return res

    def get_confirm(self, data):
        return data.head.is_confirmed

    def can_view(self):
        if PermissionController.is_admin(self.http_request.user):
            return True
        return False
