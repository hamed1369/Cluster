from django.conf.urls import patterns, url

urlpatterns = patterns('cluster.utils.manager.views',
                       url(r'^(?P<manager_name>\w+)/$', 'process_main_page', name='process_manager'),
                       url(r'^(?P<manager_name>\w+)/actions/$', 'process_actions', name='process_manager_actions'),

)
