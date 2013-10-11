# -*- coding: utf-8 -*-
from django import forms
from cluster.account.account.models import Arbiter
from cluster.account.actions import ArbiterInvitationAction
from cluster.registration.forms import ArbiterForm, AdminEditArbiter
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.action import DeleteAction, AddAction, EditAction, ShowAction, ConfirmAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class ArbiterFilterForm(ClusterBaseModelForm):
    class Meta:
        model = Arbiter
        fields = ('workplace', 'interested_domain', 'is_confirmed')

    def __init__(self, *args, **kwargs):
        super(ArbiterFilterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(label=u"نام", required=False)
        self.fields['last_name'] = forms.CharField(label=u"نام خانوادگی", required=False)
        self.fields['is_confirmed'] = forms.NullBooleanField(required=False, label=u"تایید شده")
        self.fields['is_confirmed'].widget.choices = ((u'1', u"--- همه ---"),
                                                   (u'2', u"بله"),
                                                   (u'3', u"خیر"))


class ArbiterManager(ObjectsManager):
    manager_name = u"arbiters_management"
    manager_verbose_name = u"داوران"
    filter_form = ArbiterFilterForm

    actions = [AddAction(ArbiterForm), EditAction(AdminEditArbiter), ShowAction(AdminEditArbiter), DeleteAction(),
               ConfirmAction('is_confirmed'), ArbiterInvitationAction()]

    def get_all_data(self):
        return Arbiter.objects.filter(invited=False)

    def get_columns(self):
        columns = [
            ManagerColumn('full_name', u"نام و نام خانوادگی", '30', True),
            ManagerColumn('gender', u"جنسیت", '10'),
            ManagerColumn('national_code', u"کد ملی", '10'),
            ManagerColumn('birth_date', u"تاریخ تولد", '10'),
            ManagerColumn('workplace', u"نام محل کار", '10'),
            # ManagerColumn('field', u"رشته", '10'),
            ManagerColumn('domains', u"حوزه های مورد علاقه", '30', True),
            ManagerColumn('created_on', u"تاریخ ثبت نام", '10'),
            ManagerColumn('is_confirmed', u"تایید شده", '10'),
        ]
        return columns

    def get_full_name(self, data):
        return unicode(data)

    def get_domains(self, data):
        return u', '.join([unicode(d) for d in data.interested_domain.filter()])

    def can_view(self):
        if PermissionController.is_admin(self.http_request.user):
            return True
        return False
