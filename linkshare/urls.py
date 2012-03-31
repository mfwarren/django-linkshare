from django.conf.urls.defaults import *

urlpatterns = patterns(
    'linkshare.views',
    url(r'^stats/$', 'linkshare_stats', name='linkshare_stats'),
)

