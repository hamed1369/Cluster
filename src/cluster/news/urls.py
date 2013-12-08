from django.conf.urls import patterns, url

urlpatterns = patterns('cluster.news.views',
                       url(r'^/(?P<news_id>\d+)/$', 'news_detail', name='news_detail'),

)
