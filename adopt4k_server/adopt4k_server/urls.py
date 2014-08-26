from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r'^api/ozstatus/', 'api.views.ozstatus'),
    url(r'^tools/cleanup/', 'facade.views.cleanup_adoptions'),
    url(r'^tools/download/', 'facade.views.download'),
    url(r'',TemplateView.as_view(template_name="facade/index.html")),
)
