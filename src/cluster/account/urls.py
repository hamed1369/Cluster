# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^login/$', 'cluster.account.views.auth.login_view', name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
)
