# -*- coding: utf-8 -*-
from cluster.news.forms import NewsForm, NewsShowForm, LinkForm, LinkShowForm
from cluster.news.models import News, Link
from cluster.utils.forms import ClusterBaseModelForm, ClusterFilterModelForm
from cluster.utils.manager.action import DeleteAction, ShowAction, AddAction, EditAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn

__author__ = 'M.Y'


class NewsFilterForm(ClusterFilterModelForm):
    class Meta:
        model = News
        fields = ('title', 'publish_date')


def save_news(http_request, instance):
    instance.creator = http_request.user
    instance.save()


class MessageManager(ObjectsManager):
    manager_name = u"news_manager"
    manager_verbose_name = u"اخبار"
    filter_form = NewsFilterForm
    actions = [
        AddAction(NewsForm, save_def=save_news),
        EditAction(NewsForm),
        ShowAction(NewsShowForm, height='350'),
        DeleteAction(),
    ]

    def get_all_data(self):
        return News.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", 7),
            ManagerColumn('body', u"متن", 20, True),
            ManagerColumn('created_on', u"تاریخ ایجاد", 3),
            ManagerColumn('publish_date', u"تاریخ انتشار", 3),
        ]
        return columns

    def get_body(self, obj):
        body = obj.body.replace('\r\n', ' ').replace('\n\r', ' ').replace('\r', ' ').replace('\n', ' ')
        if len(body) > 45:
            body = body[:45] + ' ...'
        return body



class LinkFilterForm(ClusterFilterModelForm):
    class Meta:
        model = Link
        fields = ('title', 'url')


class LinkManager(ObjectsManager):
    manager_name = u"links_manager"
    manager_verbose_name = u"لینک ها"
    filter_form = LinkFilterForm
    actions = [
        AddAction(LinkForm),
        EditAction(LinkForm),
        ShowAction(LinkShowForm, height='350'),
        DeleteAction(),
    ]

    def get_all_data(self):
        return Link.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('title', u"عنوان", 12),
            ManagerColumn('url', u"لینک", 12),
            ManagerColumn('order', u"ترتیب نمایش", 3),
            ManagerColumn('created_on', u"تاریخ ایجاد", 4),
        ]
        return columns
