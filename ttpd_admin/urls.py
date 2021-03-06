# urls.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

from django.conf.urls import url
from .views import (
  ActivityLogsList,
  IndustriesCreate,
  IndustriesDelete,
  IndustriesList,
  IndustriesUpdate,
  SectorsCreate,
  SectorsDelete,
  SectorsList,
  SectorsUpdate,
  ISPsCreate,
  ISPsDelete,
  ISPsList,
  ISPsUpdate,
  ProtectionTypesCreate,
  ProtectionTypesDelete,
  ProtectionTypesList,
  ProtectionTypesUpdate,
  PotentialAdoptersCreate,
  PotentialAdoptersDelete,
  PotentialAdoptersList,
  PotentialAdoptersUpdate,
  AdopterTypesCreate,
  AdopterTypesDelete,
  AdopterTypesList,
  AdopterTypesUpdate,
  AdoptersCreate,
  AdoptersDelete,
  AdoptersList,
  AdoptersUpdate,
  FundingTypesCreate,
  FundingTypesDelete,
  FundingTypesList,
  FundingTypesUpdate,
  AgencyTypesCreate,
  AgencyTypesDelete,
  AgencyTypesList,
  AgencyTypesUpdate,
  AdoptersUpdate,
  AgenciesCreate,
  AgenciesDelete,
  AgenciesList,
  AgenciesUpdate,
  GeneratorsCreate,
  GeneratorsDelete,
  GeneratorsList,
  GeneratorsUpdate,
  TechCategoriesCreate,
  TechCategoriesDelete,
  TechCategoriesList,
  TechCategoriesUpdate,
  TechnologiesCreate,
  TechnologiesDetails,
  TechnologiesDelete,
  TechnologiesList,
  TechnologiesUpdate,
  UsersProfile,
  UsersList,
  UsersCreate,
  UsersDelete,
  UsersUpdate,
  RegisteredUsersList
)

urlpatterns = [
  url(r'^activity-logs/$', ActivityLogsList.as_view(), name='activity_logs_list'),

  url(r'^data-management/industries/$',
      IndustriesList.as_view(),
      name='industries_list'),
  url(r'^data-management/industries/add/$',
      IndustriesCreate.as_view(),
      name='industries_create'),
  url(r'^data-management/industries/(?P<pk>\d+)/$',
      IndustriesUpdate.as_view(),
      name='industries_update'),
  url(r'^data-management/industries/(?P<pk>\d+)/delete$',
      IndustriesDelete.as_view(),
      name='industries_delete'),

  url(r'^data-management/industries-sectors/$',
      SectorsList.as_view(),
      name='sectors_list'),
  url(r'^data-management/industries-sectors/add/$',
      SectorsCreate.as_view(),
      name='sectors_create'),
  url(r'^data-management/industries-sectors/(?P<pk>\d+)/$',
      SectorsUpdate.as_view(),
      name='sectors_update'),
  url(r'^data-management/industries-sectors/(?P<pk>\d+)/delete$',
      SectorsDelete.as_view(),
      name='sectors_delete'),

  url(r'^data-management/industries-isps/$',
      ISPsList.as_view(),
      name='isps_list'),
  url(r'^data-management/industries-isps/add/$',
      ISPsCreate.as_view(),
      name='isps_create'),
  url(r'^data-management/industries-isps/(?P<pk>\d+)/$',
      ISPsUpdate.as_view(),
      name='isps_update'),
  url(r'^data-management/industries-isps/(?P<pk>\d+)/delete$',
      ISPsDelete.as_view(),
      name='isps_delete'),

  url(r'^data-management/protection-types/$',
      ProtectionTypesList.as_view(),
      name='protection_types_list'),
  url(r'^data-management/protection-types/add/$',
      ProtectionTypesCreate.as_view(),
      name='protection_types_create'),
  url(r'^data-management/protection-types/(?P<pk>\d+)/$',
      ProtectionTypesUpdate.as_view(),
      name='protection_types_update'),
  url(r'^data-management/protection-types/(?P<pk>\d+)/delete$',
      ProtectionTypesDelete.as_view(),
      name='protection_types_delete'),

  url(r'^data-management/potential-adopters/$',
      PotentialAdoptersList.as_view(),
      name='potential_adopters_list'),
  url(r'^data-management/potential-adopters/add/$',
      PotentialAdoptersCreate.as_view(),
      name='potential_adopters_create'),
  url(r'^data-management/potential-adopters/(?P<pk>\d+)/$',
      PotentialAdoptersUpdate.as_view(),
      name='potential_adopters_update'),
  url(r'^data-management/potential-adopters/(?P<pk>\d+)/delete$',
      PotentialAdoptersDelete.as_view(),
      name='potential_adopters_delete'),

  url(r'^data-management/adopter-types/$',
      AdopterTypesList.as_view(),
      name='adopter_types_list'),
  url(r'^data-management/adopter-types/add/$',
      AdopterTypesCreate.as_view(),
      name='adopter_types_create'),
  url(r'^data-management/adopter-types/(?P<pk>\d+)/$',
      AdopterTypesUpdate.as_view(),
      name='adopter_types_update'),
  url(r'^data-management/adopter-types/(?P<pk>\d+)/delete$',
      AdopterTypesDelete.as_view(),
      name='adopter_types_delete'),

  url(r'^data-management/adopters/$',
      AdoptersList.as_view(),
      name='adopters_list'),
  url(r'^data-management/adopters/add/$',
      AdoptersCreate.as_view(),
      name='adopters_create'),
  url(r'^data-management/adopters/(?P<pk>\d+)/$',
      AdoptersUpdate.as_view(),
      name='adopters_update'),
  url(r'^data-management/adopters/(?P<pk>\d+)/delete$',
      AdoptersDelete.as_view(),
      name='adopters_delete'),

  url(r'^data-management/funding-types/$',
      FundingTypesList.as_view(),
      name='funding_types_list'),
  url(r'^data-management/funding-types/add/$',
      FundingTypesCreate.as_view(),
      name='funding_types_create'),
  url(r'^data-management/funding-types/(?P<pk>\d+)/$',
      FundingTypesUpdate.as_view(),
      name='funding_types_update'),
  url(r'^data-management/funding-types/(?P<pk>\d+)/delete$',
      FundingTypesDelete.as_view(),
      name='funding_types_delete'),

  url(r'^data-management/agency-types/$',
      AgencyTypesList.as_view(),
      name='agency_types_list'),
  url(r'^data-management/agency-types/add/$',
      AgencyTypesCreate.as_view(),
      name='agency_types_create'),
  url(r'^data-management/agency-types/(?P<pk>\d+)/$',
      AgencyTypesUpdate.as_view(),
      name='agency_types_update'),
  url(r'^data-management/agency-types/(?P<pk>\d+)/delete$',
      AgencyTypesDelete.as_view(),
      name='agency_types_delete'),

  url(r'^data-management/agencies/$',
      AgenciesList.as_view(),
      name='agencies_list'),
  url(r'^data-management/agencies/add/$',
      AgenciesCreate.as_view(),
      name='agencies_create'),
  url(r'^data-management/agencies/(?P<pk>\d+)/$',
      AgenciesUpdate.as_view(),
      name='agencies_update'),
  url(r'^data-management/agencies/(?P<pk>\d+)/delete$',
      AgenciesDelete.as_view(),
      name='agencies_delete'),

  url(r'^data-management/generators/$',
      GeneratorsList.as_view(),
      name='generators_list'),
  url(r'^data-management/generators/add/$',
      GeneratorsCreate.as_view(),
      name='generators_create'),
  url(r'^data-management/generators/(?P<pk>\d+)/$',
      GeneratorsUpdate.as_view(),
      name='generators_update'),
  url(r'^data-management/generators/(?P<pk>\d+)/delete$',
      GeneratorsDelete.as_view(),
      name='generators_delete'),

  url(r'^data-management/technology-categories/$',
      TechCategoriesList.as_view(),
      name='tech_categories_list'),
  url(r'^data-management/technology-categories/add/$',
      TechCategoriesCreate.as_view(),
      name='tech_categories_create'),
  url(r'^data-management/technology-categories/(?P<pk>\d+)/$',
      TechCategoriesUpdate.as_view(),
      name='tech_categories_update'),
  url(r'^data-management/technology-categories/(?P<pk>\d+)/delete$',
      TechCategoriesDelete.as_view(),
      name='tech_categories_delete'),

  # url(r'^technologies/$',
  #     TechnologiesList.as_view(),
  #     name='technologies_list'),

  url(r'^$',
      TechnologiesList.as_view(),
      name='technologies_list'),
  url(r'^technologies/add/$',
      TechnologiesCreate.as_view(),
      name='technologies_create'),
  url(r'^technologies/(?P<pk>\d+)/edit$',
      TechnologiesUpdate.as_view(),
      name='technologies_update'),
  url(r'^technologies/(?P<pk>\d+)/delete$',
      TechnologiesDelete.as_view(),
      name='technologies_delete'),
  url(r'^technologies/(?P<pk>\d+)$',
      TechnologiesDetails.as_view(),
      name='technologies_details'),

  url(r'^users/$',
      UsersList.as_view(),
      name='users_list'),
  url(r'^profile/(?P<pk>\d+)/$',
      UsersProfile.as_view(),
      name='users_profile'),
  url(r'^users/add/$',
      UsersCreate.as_view(),
      name='users_create'),
  url(r'^users/(?P<pk>\d+)/$',
      UsersUpdate.as_view(),
      name='users_update'),
  url(r'^users/(?P<pk>\d+)/delete$',
      UsersDelete.as_view(),
      name='users_delete'),

  url(r'^users/registered/$',
      RegisteredUsersList.as_view(),
      name='users_registered_list'),
]


