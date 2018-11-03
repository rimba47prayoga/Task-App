from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PaginationTotalPages(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        uri = self.request.build_absolute_uri().split('?')[0]
        pages = [x for x in range(1, self.page.paginator.num_pages + 1)]

        total_pages = len(pages)

        return Response({
            'next': self.get_next_link(),
            'base_link': uri + '?page=',
            'previous': self.get_previous_link(),
            'pages': pages,
            'count': self.page.paginator.count,
            'current_page': self.page.number,
            'start_index': self.page.start_index(),
            'end_index': self.page.end_index(),
            'results': data,
            'total_pages': total_pages
        })
