# -*- coding: utf-8 -*-
from cluster.feedback.forms import FeedbackShowForm, ContactShowForm
from cluster.feedback.models import Feedback, ContactUs
from cluster.utils.forms import ClusterFilterModelForm
from cluster.utils.manager.action import DeleteAction, ShowAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn

__author__ = 'M.Y'


class FeedbackFilterForm(ClusterFilterModelForm):
    class Meta:
        model = Feedback
        fields = ('title', 'creator')


class FeedbackManager(ObjectsManager):
    manager_name = u"feedback_manager"
    manager_verbose_name = u"مشاهده نظرات و پیشنهادات"
    filter_form = FeedbackFilterForm
    actions = [
        DeleteAction(),
        ShowAction(FeedbackShowForm, height='350'),
    ]

    def get_all_data(self):
        return Feedback.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", 7),
            ManagerColumn('body', u"متن", 20, True),
            ManagerColumn('creator', u"ایجادکننده", 3),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
            ManagerColumn('feeder', u"پیشنهاددهنده", 3, True, True),
            ManagerColumn('cluster_feeder', u"خوشه پیشنهاددهنده", 5, True, True),
        ]
        return columns

    def get_body(self, obj):
        body = obj.body.replace('\r\n', ' ').replace('\n\r', ' ').replace('\r', ' ').replace('\n', ' ')
        if len(body) > 45:
            body = body[:45] + ' ...'
        return body

    def get_feeder(self, data):
        from cluster.account.account.models import Member

        try:
            link = u"/members/actions/?t=action&n=edit_member&i=%s" % data.creator.member.id
            return u"""<a onClick="MyWindow=window.open('%s','خوشه/فرد',width=800,height=600); return false;"href='#' class="jqgrid-a">%s</a>""" % (
                link, unicode(data.creator.member))
        except Member.DoesNotExist:
            return None

    def get_cluster_feeder(self, data):
        from cluster.account.account.models import Member, Cluster

        try:
            if data.creator.member.cluster:
                link = u"/clusters/actions/?t=action&n=edit_cluster&i=%s" % data.creator.member.cluster.id
                return u"""<a onClick="MyWindow=window.open('%s','خوشه/فرد',width=800,height=600); return false;"href='#' class="jqgrid-a">%s</a>""" % (
                    link, unicode(data.creator.member.cluster))
        except (Member.DoesNotExist, Cluster.DoesNotExist):
            return None


class ContactFilterForm(ClusterFilterModelForm):
    class Meta:
        model = ContactUs
        fields = ('title', 'email')


class ContactManager(ObjectsManager):
    manager_name = u"contact_manager"
    manager_verbose_name = u"تماس ها"
    filter_form = ContactFilterForm
    actions = [
        DeleteAction(),
        ShowAction(ContactShowForm, height='350'),
    ]

    def get_all_data(self):
        return ContactUs.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", 7),
            ManagerColumn('body', u"متن", 20, True),
            ManagerColumn('email', u"پست الکترونیک", 7),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
        ]
        return columns

    def get_body(self, obj):
        body = obj.body.replace('\r\n', ' ').replace('\n\r', ' ').replace('\r', ' ').replace('\n', ' ')
        if len(body) > 45:
            body = body[:45] + ' ...'
        return body
