from django.conf.urls import patterns, url

urlpatterns = patterns('cluster.project.views',
                       # url(r'^$', '.index', name='index'),
                       url(r'^register/$', 'register', name='project_register'),
                       url(r'^view_arbiter_comment/(?P<project_arbiter_id>\d+)/$', 'view_arbiter_comment', name='view_arbiter_comment'),

)
