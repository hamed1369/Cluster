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

                       # Uncomment the admin/doc line below to enable admin documentation:
                       #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/', include('cluster.account.urls')),
                       url(r'^project/', include('cluster.project.urls')),
                       url(r'^manager/', include('cluster.utils.manager.urls')),
                       url(r'^ajax/', include('cluster.utils.ajax.urls')),

)

urlpatterns += patterns('',
                        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                         {'document_root': settings.STATIC_ROOT}),
)

urlpatterns += patterns('',
                        url(r'^captcha/', include('captcha.urls')),
)
manager.register_children()
