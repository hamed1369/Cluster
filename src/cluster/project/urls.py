from django.conf.urls import patterns, url

urlpatterns = patterns('cluster.project.views',
                       # url(r'^$', '.index', name='index'),
                       url(r'^register/$', 'register', name='project_register'),

)
