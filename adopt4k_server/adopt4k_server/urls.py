from django.conf.urls import patterns, include, url
from rest_framework import routers
from api import views
from facade import views as facade_views

from django.contrib import admin
admin.autodiscover()


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'ozfeatures', views.OZFeatureViewSet)
router.register(r'adoptions', views.AdoptionViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'adopt4k_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r'^$', facade_views.index),
)
