from django.conf.urls import patterns, url

urlpatterns = patterns('cluster.news.views',
                       url(r'^/archive/$', 'archive', name='archive'),
                       url(r'^/(?P<news_id>\d+)/$', 'news_detail', name='news_detail'),

)
