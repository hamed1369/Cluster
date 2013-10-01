# -*- coding: utf-8 -*-
from cluster.news.forms import NewsForm, NewsShowForm
from cluster.news.models import News
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.action import DeleteAction, ShowAction, AddAction, EditAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn

__author__ = 'M.Y'


class NewsFilterForm(ClusterBaseModelForm):
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
