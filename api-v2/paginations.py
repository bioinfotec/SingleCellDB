from rest_framework.pagination import PageNumberPagination,Response
from rest_framework_datatables.pagination import DatatablesPageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10  # 每页显示的数据条数
    page_size_query_param = "page_size"  # URL参数中指定每页显示的数据条数的参数名
    max_page_size = 100  # 每页显示的最大数据条数
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })

class CustomeDatabalesPagination(DatatablesPageNumberPagination):
    pass