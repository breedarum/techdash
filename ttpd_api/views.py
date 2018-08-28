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
from ttpd_admin.models import Commodities, Industries, User
from .paginations import ConditionalPagination, DefaultPagination
from .serializers import (
  CommoditiesSerializer,
  IndustriesSerializer,
  UsersSerializer
)

# a homepage for the api
def blank_index(request):
    data = {
      'message': 'Welcome to the API homepage!'
    }

    return HttpResponse(json.dumps(data), content_type='application/json')
    #return render(request, 'templates/commodities.html')

class CommoditiesList(generics.ListAPIView, ConditionalPagination):
    queryset = Commodities.objects.all().order_by('name')
    serializer_class = CommoditiesSerializer
    pagination_class = DefaultPagination

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

class CommoditiesDetail(generics.RetrieveAPIView):
    queryset = Commodities.objects.all()
    serializer_class = CommoditiesSerializer

class IndustriesList(generics.ListAPIView, ConditionalPagination):
    queryset = Industries.objects.all()
    serializer_class = IndustriesSerializer
    pagination_class = DefaultPagination

class IndustriesDetail(generics.RetrieveAPIView):
    queryset = Industries.objects.all()
    serializer_class = IndustriesSerializer

# /auth/register
class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (permissions.AllowAny,)


