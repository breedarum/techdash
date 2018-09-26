# views.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

import json
from django.views import View
from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rolepermissions.roles import get_user_roles
from rolepermissions.checkers import has_role, has_permission
from rolepermissions.mixins import HasPermissionsMixin, HasRoleMixin
from ttpd.roles import *
from ttpd_admin.models import Industries, User, ProtectionLevels, TechCategories, Technologies, TechnologyStatuses
from .paginations import ConditionalPagination, DefaultPagination
from .serializers import (
  IndustriesSerializer,
  ProtectionTypesSerializer,
  TechnologyCategoriesSerializer,
  TechnologiesSerializerFirstLevel,
  TechnologiesSerializerSecondLevel,
  TechnologiesSerializerThirdLevel,
  TechnologiesSearchSerializer,
  UsersSerializer
)

# a homepage for the api
def blank_index(request):
    data = {
      'message': 'Welcome to the API homepage!'
    }

    return HttpResponse(json.dumps(data), content_type='application/json')
    #return render(request, 'templates/commodities.html')

class IndustriesList(generics.ListAPIView, ConditionalPagination):
    queryset = Industries.objects.all()
    serializer_class = IndustriesSerializer
    pagination_class = DefaultPagination

class IndustriesDetail(generics.RetrieveAPIView):
    queryset = Industries.objects.all()
    serializer_class = IndustriesSerializer

class ISPsDetail(generics.RetrieveAPIView):
    queryset = Industries.objects.all()
    serializer_class = IndustriesSerializer

class ProtectionLevelsList(generics.ListAPIView, ConditionalPagination):
    queryset = ProtectionLevels.objects.all()
    serializer_class = ProtectionTypesSerializer
    pagination_class = DefaultPagination

class TechnologyCategoriesList(generics.ListAPIView, ConditionalPagination):
    queryset = TechCategories.objects.all()
    serializer_class = TechnologyCategoriesSerializer
    pagination_class = DefaultPagination

class TechnologyCategoriesDetail(generics.RetrieveAPIView):
    queryset = TechCategories.objects.all()
    serializer_class = TechnologyCategoriesSerializer

class TechnologiesList(generics.ListAPIView, ConditionalPagination):
    pagination_class = DefaultPagination
    allowed_filters = [ 'year', 
                        'industry_sector_isps', 
                        'categories', 
                        'protection_level', 
                        'adopters', 
                        'generators', 
                        'owners', 
                        'statuses', 
                        'fundings',
                        'protection_types' ]


    def get_serializer_class(self):

        if self.request.user.is_superuser:
             return TechnologiesSerializerThirdLevel
        if self.request.user.is_staff:
             return TechnologiesSerializerSecondLevel

        return TechnologiesSerializerFirstLevel

    def get_queryset(self):

        queryset = Technologies.objects.all()
        sort_request = self.request.query_params.get('sort', None)

        # loop through all of the allowed filters and look for it in the request query parameters
        # if present, apply the filter to the queryset
        for allowed_filter in self.allowed_filters:
            filter_param = self.request.query_params.get(allowed_filter, None)

            if filter_param is None:
                continue

            if allowed_filter == 'year':
                queryset = queryset.filter(year=filter_param)

            if allowed_filter == 'industry_sector_isps':
                queryset = queryset.filter(industry_sector_isps__name__in=filter_param.split(','))

            if allowed_filter == 'categories':
                queryset = queryset.filter(categories__name__in=filter_param.split(','))

            if allowed_filter == 'protection_level':
                queryset = queryset.filter(protection_level__name=filter_param)

            if allowed_filter == 'adopters':
                queryset = queryset.filter(adopter__name=filter_param)

            if allowed_filter == 'generators':
                queryset = queryset.filter(generators__title=filter_param)

            if allowed_filter == 'owners':
                queryset = queryset.filter(owners__name=filter_param)

            if allowed_filter == 'statuses':
                queryset = queryset.filter(statuses__name=filter_param)

            if allowed_filter == 'fundings':
                queryset = queryset.filter(fundings__name=filter_param)

            if allowed_filter == 'protection_types':
                queryset = queryset.filter(protection_types__name=filter_param)

        # if sort query parameter is present, perform sorting by issuing the correct SQL / Django Queryset
        if sort_request is not None:
            sort_params = sort_request.split(',')

            # TODO: refactor this condition! inefficient checking of allowed sort params!
            if 'name' in sort_params or 'year' in sort_params:
                queryset = queryset.order_by(*sort_params)

        return queryset

class TechnologiesSearch(generics.ListAPIView, ConditionalPagination):
    pagination_class = DefaultPagination
    serializer_class = TechnologiesSearchSerializer
    allowed_filters = [ 'id',
                        'url',
                        'title',
                        'year',
                        'description',
                        'region',
                        'categories',
                        'industry_sector_isps'
                        ]

    def get_queryset(self):

        queryset = Technologies.objects.all()
        sort_request = self.request.query_params.get('sort', None)

        # loop through all of the allowed filters and look for it in the request query parameters
        # if present, apply the filter to the queryset
        for allowed_filter in self.allowed_filters:
            filter_param = self.request.query_params.get(allowed_filter, None)

            if filter_param is None:
                continue

            if allowed_filter == 'year':
                queryset = queryset.filter(year=filter_param)

            if allowed_filter == 'industry_sector_isps':
                queryset = queryset.filter(industry_sector_isps__name__in=filter_param.split(','))

            if allowed_filter == 'categories':
                queryset = queryset.filter(categories__name__in=filter_param.split(','))

        # if sort query parameter is present, perform sorting by issuing the correct SQL / Django Queryset
        if sort_request is not None:
            sort_params = sort_request.split(',')

            # TODO: refactor this condition! inefficient checking of allowed sort params!
            if 'name' in sort_params or 'year' in sort_params:
                queryset = queryset.order_by(*sort_params)

        return queryset

class TechnologiesDetail(generics.RetrieveAPIView):
    queryset = Technologies.objects.all()

    def get_serializer_class(self):

        if self.request.user.is_superuser:
             return TechnologiesSerializerThirdLevel
        if self.request.user.is_staff:
             return TechnologiesSerializerSecondLevel

        return TechnologiesSerializerFirstLevel

# CBV for returning list of years that are encoded with the technologies
class TechnologYearsList(View):

    def get(self, _):
        queryset = Technologies.objects.distinct().values_list('year')

        data = [item for sublist in list(queryset) for item in sublist]

        return HttpResponse(json.dumps(data), content_type='application/json')

# /auth/register
class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (permissions.AllowAny,)


