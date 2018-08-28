# paginations.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

from collections import OrderedDict
from rest_framework import mixins, pagination
from rest_framework.response import Response

class DefaultPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
          ('total', self.page.paginator.count),
          ('per_page', self.page.paginator.per_page),
          ('next', self.get_next_link()),
          ('previous', self.get_previous_link()),
          ('results', data)
        ]))

class ConditionalPagination(mixins.ListModelMixin):

    # Override list method to conditionally disable pagination
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        disable_pagination = request.query_params.get('disable_pagination', False)

        if isinstance(disable_pagination, str) and disable_pagination.lower() == 'true':
            disable_pagination = True
        else:
            disable_pagination = False

        page = self.paginate_queryset(queryset)
        if page is not None and disable_pagination is False:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


