"""ttpd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from ttpd_admin import admin
from ttpd_api import urls as ttpd_api_urls

from rest_framework import routers
from ttpd_api import views


router = routers.DefaultRouter()
router.register(r'commodities', views.CommoditiesList)
router.register(r'industries', views.CommoditiesList)

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  url(r'^api/', include(ttpd_api_urls)),
]

# add the debug toolbar to the path when DEBUG is set to true
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
      url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


