from rest_framework.response import Response
from rest_framework.decorators import api_view
from celldb.models import TranMeta, DataSetMeta
from .serializers import TranMetaSerializer, DataSetMetaSerializer
from .paginations import CustomPagination
from rest_framework import status
from rest_framework.viewsets import ModelViewSet


class DataSetView(ModelViewSet):
    queryset = DataSetMeta.objects.order_by("dataset_id")
    serializer_class = DataSetMetaSerializer


@api_view(["GET"])
def getTran(request, formar=None):
    paginator = CustomPagination()
    data = TranMeta.objects.order_by("data_id")
    result_page = paginator.paginate_queryset(data, request)
    serializer = TranMetaSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def getTran_all(request, formar=None):
    data = TranMeta.objects.all()
    serializer = TranMetaSerializer(data, many=True)
    return Response(serializer.data)


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
