# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('cluster.account.views',
                       url(r'^login_view/$', 'auth.login_view', name='index'),
                       url(r'^signup/$', 'auth.signup', name='index'),

)
