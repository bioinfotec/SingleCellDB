from rest_framework.response import Response
from rest_framework.decorators import api_view
from celldb.models import TranMeta
from .serializers import TranMetaSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView


class CustomPagination(PageNumberPagination):
    page_size = 10  # 每页显示的数据条数
    page_size_query_param = "page_size"  # URL参数中指定每页显示的数据条数的参数名
    max_page_size = 100  # 每页显示的最大数据条数


@api_view(["GET"])
def getTran(request, formar=None):
    paginator = CustomPagination()
    data = TranMeta.objects.all()
    result_page = paginator.paginate_queryset(data, request)
    serializer = TranMetaSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET", "POST", "DELETE"])
def getTran_detail(request, id, format=None):
    try:
        tran = TranMeta.objects.get(data_id=id)
    except TranMeta.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TranMetaSerializer(tran)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TranMetaSerializer(tran, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == "DELETE":
        tran.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 过滤功能
class MyView(APIView):
    filter_backends = [OrderingFilter]
    ordering_fields = ["cell_type"]  # 指定可排序的字段列表

    def get(self, request):
        # 处理 GET 请求的逻辑
        # 获取排序参数
        ordering = self.request.query_params.get("ordering")

        # 执行排序逻辑
        if ordering:
            # 根据排序参数对数据进行排序
            queryset = TranMeta().objects.all().order_by(ordering)
        else:
            # 默认排序逻辑
            queryset = TranMeta().objects.all().order_by("id")

        # 返回排序结果
        serializer = TranMetaSerializer(queryset, many=True)
        return Response(serializer.data)
