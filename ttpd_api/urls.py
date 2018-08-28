# urls.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_jwt.views import obtain_jwt_token
from .views import (
  blank_index,
  CommoditiesDetail,
  CommoditiesList,
  IndustriesDetail,
  IndustriesList,
  UserRegister
)

urlpatterns = [
  url(r'^$', blank_index, name='api_index'),
  url(r'commodities/$', CommoditiesList.as_view(), name='api_commodities_list'),
  url(r'commodities/(?P<pk>[0-9]+)/$', CommoditiesDetail.as_view(), name='api_commodities_detail'),
  url(r'industries/$', IndustriesList.as_view(), name='api_industries_list'),
  url(r'industries/(?P<pk>[0-9]+)/$', IndustriesDetail.as_view(), name='api_industries_detail'),
  url(r'auth/register$', UserRegister.as_view(), name='api_user_register'),
  url(r'auth/login$', obtain_jwt_token, name='api_user_login'),
]

urlpatterns = format_suffix_patterns(urlpatterns)


