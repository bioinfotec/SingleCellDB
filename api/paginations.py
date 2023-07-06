from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 4  # 每页显示的数据条数
    page_size_query_param = "page_size"  # URL参数中指定每页显示的数据条数的参数名
    max_page_size = 100000  # 每页显示的最大数据条数
