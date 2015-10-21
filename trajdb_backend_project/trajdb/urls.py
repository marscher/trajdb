"""trajdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin

from apps.trajdb import views
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [url(r'^admin/', include(admin.site.urls)),
               ]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

router = DefaultRouter()
router.register(r'collections', views.CollectionViewSet, 'collection')
router.register(r'meta-collections', views.SetupViewSet, 'meta-collection')
router.register(r'trajectories', views.TrajectoryViewSet, 'trajectory')
router.register(r'setups', views.SetupViewSet, 'setup')
router.register(r'users', views.UserViewSet, 'user')

urlpatterns += router.urls

# enable download of uploaded files in debug environment:
if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^download/(?P<path>.*)$',
                             'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT}))
else:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
