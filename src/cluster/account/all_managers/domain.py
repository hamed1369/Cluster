# -*- coding: utf-8 -*-
from django import forms
from cluster.account.account.models import Domain
from cluster.utils.forms import ClusterBaseModelForm, ClusterFilterModelForm
from cluster.utils.manager.action import AddAction, EditAction, DeleteAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class DomainActionForm(ClusterBaseModelForm):
    class Meta:
        model = Domain
        fields = ('name', 'confirmed')


class DomainForm(ClusterFilterModelForm):
    class Meta:
        model = Domain
        fields = ('name', 'confirmed')

    def __init__(self, *args, **kwargs):
        super(DomainForm, self).__init__(*args, **kwargs)
        self.fields['confirmed'] = forms.NullBooleanField(required=False, label=u"تایید شده")
        self.fields['confirmed'].widget.choices = ((u'1', u"--- همه ---"),
                                                   (u'2', u"بله"),
                                                   (u'3', u"خیر"))


class DomainManager(ObjectsManager):
    manager_name = u"domains"
    manager_verbose_name = u"مدیریت حوزه ها"
    filter_form = DomainForm
    actions = [AddAction(DomainActionForm), EditAction(DomainActionForm, action_verbose_name=u"بررسی و ویرایش"),
               DeleteAction()]

    def get_all_data(self):
        return Domain.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('name', u"نام حوزه", '10'),
            ManagerColumn('confirmed', u"تایید شده", '10'),
            ManagerColumn('requester', u"درخواست دهنده", '10', True, True),
        ]
        return columns

    def can_view(self):
        if PermissionController.is_admin(self.http_request.user):
            return True
        return False

    def get_requester(self, data):
        if not data.confirmed:
            clusters = data.clusters.all()
            if clusters:
                link = u"/clusters/actions/?t=action&n=edit_cluster&i=%s" % clusters[0].id
                return u"""<a onClick="MyWindow=window.open('%s','خوشه/فرد',width=800,height=600); return false;"href='#' class="jqgrid-a">%s</a>""" % (
                    link, unicode(clusters[0]))
        return None