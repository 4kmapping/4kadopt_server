from django.conf.urls import patterns, include, url

urlpatterns = patterns('mobile.views',
    url(r'^ozlist', 'ozlist'),
    url(r'^ozstatus','ozstatus'),
)
