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
  ProtectionLevelsDetail,
  ProtectionLevelsList,
  TechnologyCategoriesDetail,
  TechnologyCategoriesList,
  TechnologiesDetail,
  TechnologiesList,
  TechnologYearsList,
  UserRegister
)

urlpatterns = [
  url(r'^$', blank_index, name='api_index'),
  url(r'commodities/$', CommoditiesList.as_view(), name='api_commodities_list'),
  url(r'commodities/(?P<pk>[0-9]+)/$', CommoditiesDetail.as_view(), name='api_commodities_detail'),
  url(r'industries/$', IndustriesList.as_view(), name='api_industries_list'),
  url(r'industries/(?P<pk>[0-9]+)/$', IndustriesDetail.as_view(), name='api_industries_detail'),
  url(r'protection-levels/$', ProtectionLevelsList.as_view(), name='api_protection_levels_list'),
  url(r'protection-levels/(?P<pk>[0-9]+)/$', ProtectionLevelsDetail.as_view(), name='api_protection_levels_detail'),
  url(r'technology-categories/$', TechnologyCategoriesList.as_view(), name='api_technology_categories_list'),
  url(r'technology-categories/(?P<pk>[0-9]+)/$', TechnologyCategoriesDetail.as_view(), name='api_technology_categories_detail'),
  url(r'technologies/$', TechnologiesList.as_view(), name='api_technologies_list'),
  url(r'technologies/(?P<pk>[0-9]+)/$', TechnologiesDetail.as_view(), name='api_technologies_detail'),
  url(r'technologies/years$', TechnologYearsList.as_view(), name='api_technology_years_list'),
  
  url(r'auth/register$', UserRegister.as_view(), name='api_user_register'),
  url(r'auth/login$', obtain_jwt_token, name='api_user_login'),
]

urlpatterns = format_suffix_patterns(urlpatterns)


