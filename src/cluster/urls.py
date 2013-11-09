from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from cluster import settings
from cluster.utils import manager

admin.autodiscover()

urlpatterns = patterns('',
                       # url(r'^$', 'cluster.views.home', name='home'),
                       url(r'^', include('cluster.registration.urls')),
                       url(r'^$', 'cluster.account.views.index.index', name='index'),
                       url(r'^feedback/$', 'cluster.feedback.views.send_feedback', name='feedback'),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/', include('cluster.account.urls')),
                       url(r'^project/', include('cluster.project.urls')),
                       url(r'^ajax/', include('cluster.utils.ajax.urls')),
                       url(r'^news', include('cluster.news.urls')),

)

urlpatterns += patterns('',
                        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': settings.STATIC_ROOT}),
                        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += patterns('',
                        url(r'^captcha/', include('captcha.urls')),
                        url(r'^select2/', include('django_select2.urls')),
                        url(r'^tinymce/', include('tinymce.urls')),
)

manager.register_children()
