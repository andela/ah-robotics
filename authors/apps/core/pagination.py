from rest_framework import pagination
from rest_framework.response import Response


class ArticlesListPagination(pagination.PageNumberPagination):
    """
    Custom Paginator for Article List View
    """
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'previous': self.get_previous_link(),
            'next': self.get_next_link(),
            'articles': data
        })
