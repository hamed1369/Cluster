# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('cluster.account.views',
                       url(r'^login/$', 'auth.login_view', name='login'),
)
