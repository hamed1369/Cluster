from django.conf.urls import patterns, url

urlpatterns = patterns('cluster.utils.ajax.views',
                       url(r'^validationEngine/$', 'validationEngine', name='ajax_validationEngine'),
                       url(r'^select2/$', 'select2', name='select2'),

)
