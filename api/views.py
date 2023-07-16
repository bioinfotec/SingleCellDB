from django.http.response import JsonResponse
from celldb.models import TranMeta, DataSetMeta, LiteratureMeta,UploadedFile
from .serializers import TranMetaSerializer, DataSetMetaSerializer, LiteratureMetaSerializer,UploadedFileSerializer
from .paginations import CustomPagination
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse
import os
    
# For File download
def download_file(request):
    # 获取文件路径
    file_path = '/home/azureuser/SingleCellDB/Photo/Docker.png'  # 文件的实际路径
    file_name = os.path.basename(file_path)  # 文件名

    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError("File not found")

    # 打开文件并创建响应对象
    file = open(file_path, 'rb')
    response = FileResponse(file)

    # 设置响应头，指定文件名和内容类型
    response['Content-Disposition'] = f'attachment; filename={file_name.split("/")[-1].encode().decode("latin-1")}'
    print(f'attachment; filename={file_name.split("/")[-1].encode().decode("latin-1")}')
    response['Content-Type'] = 'application/png'  # 根据实际文件类型设置

    return response

#For Photo upload
@csrf_exempt
def SaveFiles(request):
    try:
        file = request.FILES['file']
        # 验证文件类型是否为图片
        allowed_extensions = ['txt', 'csv', 'xls', 'xlsx']
        extension = file.name.split('.')[-1].lower()
        if extension not in allowed_extensions:
            return JsonResponse({'error': '只能上传文本文件'}, status=400)
        
        file_name = default_storage.save(file.name, file)
        return JsonResponse({'message': '文件上传成功'}, status=201)
    except KeyError:
        return JsonResponse({'error': '未找到上传的文件'}, status=400)

# For FileUpload
class UploadedFileViewSet(ModelViewSet):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    parser_classes = (MultiPartParser, FormParser)
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # 列表和详情视图允许任何人访问
            permission_classes = [AllowAny]
        else:
            # 其他视图需要身份验证
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
#For DataSet
class DataSetView(ModelViewSet):
    queryset = DataSetMeta.objects.order_by("dataset_id")
    serializer_class = DataSetMetaSerializer

# For LiteratureMeta
class LiteratureMetaView(ModelViewSet):
    queryset = LiteratureMeta.objects.all()
    serializer_class = LiteratureMetaSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # 列表和详情视图允许任何人访问
            permission_classes = [AllowAny]
        else:
            # 其他视图需要身份验证
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


@api_view(["GET"])
@permission_classes([])
def getTran(request, formart=None):
    paginator = CustomPagination()
    data = TranMeta.objects.order_by("data_id")
    result_page = paginator.paginate_queryset(data, request)
    serializer = TranMetaSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@permission_classes([])
def getTran_all(request, formart=None):
    fields = request.GET.get("fields")
    if fields:
        fields = fields.split(",")
        data = TranMeta.objects.order_by("data_id").values(*fields)
    else:
        data = TranMeta.objects.all()
    serializer = TranMetaSerializer(data, many=True, fields=fields)
    import gzip,json
    from django.http import HttpResponse
    # 将序列化后的数据转换为字符串
    serialized_data = serializer.data
    json_str = json.dumps(serialized_data)

    # 使用gzip进行压缩
    compressed_data = gzip.compress(json_str.encode("utf-8"))

    # 构建gzip响应
    response = HttpResponse(content_type="application/json")
    response["Content-Encoding"] = "gzip"
    response["Content-Disposition"] = "attachment; filename=data.json.gz"

    # 将压缩后的数据写入响应
    response.write(compressed_data)

    return response

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


