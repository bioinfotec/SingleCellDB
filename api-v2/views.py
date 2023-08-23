from celldb_v2.models import literature_info, literature_dataset, dataset_info,cell_info, gene_expression,gene_info, cell_type_info, matrix_file
from .serializers import LiteratureInfoSerializer, DatasetInfoSerializer, DatasetLiteratureSerializer, LiteratureDatasetSerializer, CellInfoSerializer,GeneExpressionSerializer, GeneInfoSerializer, CellTypeInfoSerializer, DatasetLiteratureGeneSerializer,UploadedMatrixFileSerializer
from .paginations import CustomPagination,CustomeDatabalesPagination

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.renderers import DatatablesRenderer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required

# 文献信息
class LiteratureInfoView(ModelViewSet):
    queryset = literature_info.objects.all()
    serializer_class = LiteratureInfoSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # 列表和详情视图允许任何人访问
            permission_classes = [AllowAny]
        else:
            # 其他视图需要身份验证
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

# 数据信息
class DatasetInfoVeiw(ModelViewSet):
    queryset = dataset_info.objects.all()
    serializer_class = DatasetInfoSerializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # 列表和详情视图允许任何人访问
            permission_classes = [AllowAny]
        else:
            # 其他视图需要身份验证
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

# 数据-文献信息
class DatasetLiteratureVeiw(ModelViewSet):
    queryset = dataset_info.objects.all()
    serializer_class = DatasetLiteratureSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        pmid = self.request.query_params.get('pmid')
        dataset_id = self.request.query_params.get('dataset_id')
        cell_type = self.request.query_params.get('cell_type')
        specise_name = self.request.query_params.get('species')
        filters = Q()
        if pmid:
            filters &= Q(literature__pmid=pmid)
        if dataset_id:
            filters &= Q(dataset_id=dataset_id)
        if cell_type:
            filters &= Q(cell_types__icontains=cell_type)
        if specise_name:
            filters &= Q(species_name=specise_name)

        return queryset.filter(filters)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # 列表和详情视图允许任何人访问
            permission_classes = [AllowAny]
        else:
            # 其他视图需要身份验证
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
# 文献-数据信息
class LiteratureDatasetVeiw(ModelViewSet):
    queryset = literature_info.objects.all()
    serializer_class = LiteratureDatasetSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        pmid = self.request.query_params.get('pmid')
        species_name = self.request.query_params.get('species_name')
        cell_type = self.request.query_params.get('cell_type')
        filters = Q()

        if pmid:
            filters &= Q(pmid=pmid)
        
        if species_name:
            filters &= Q(dataset_info__species_name=species_name)

        if cell_type:
            filters &= Q(dataset_info__cell_types__icontains=cell_type)

        return queryset.filter(filters).distinct()
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # 列表和详情视图允许任何人访问
            permission_classes = [AllowAny]
        else:
            # 其他视图需要身份验证
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

# 细胞信息
class CellInfoView(ModelViewSet):
    serializer_class = CellInfoSerializer
    
    def get_queryset(self):
        dataset_id = self.request.query_params.get('dataset_id', None)
        queryset = cell_info.objects.filter(dataset_info_id=dataset_id)
        return queryset
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # 列表和详情视图允许任何人访问
            permission_classes = [AllowAny]
        else:
            # 其他视图需要身份验证
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

# 基因表达量
class GeneExpressionView(ModelViewSet):
    serializer_class = GeneExpressionSerializer
    
    def get_queryset(self):
        dataset_id = self.request.query_params.get('dataset_id', None)
        gene_name = self.request.query_params.get('gene_name', None)
        filters = Q()
        if gene_name == None and dataset_id == None:
            return gene_expression.objects.none()
        if gene_name:
            filters &= Q(gene_name=gene_name)
        if dataset_id:
            filters &= Q(dataset_info_id=dataset_id)
        return gene_expression.objects.filter(filters)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # 列表和详情视图允许任何人访问
            permission_classes = [AllowAny]
        else:
            # 其他视图需要身份验证
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

# 基因信息
class GeneInfoView(ModelViewSet):
    serializer_class = GeneInfoSerializer
    def get_queryset(self):
        gene_name = self.request.query_params.get('gene_name', None)
        if gene_name == None:
            return gene_info.objects.all()
        return gene_info.objects.filter(gene_name=gene_name)
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # 列表和详情视图允许任何人访问
            permission_classes = [AllowAny]
        else:
            # 其他视图需要身份验证
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

# 细胞类型表
class CellTypeView(ModelViewSet):
    queryset = cell_type_info.objects.all()
    serializer_class = CellTypeInfoSerializer
    def get_queryset(self):
        cell_type = self.request.query_params.get('cell_type', None)
        if cell_type != None:
            return cell_type_info.objects.filter(cell_type_name=cell_type)
        return self.queryset
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # 列表和详情视图允许任何人访问
            permission_classes = [AllowAny]
        else:
            # 其他视图需要身份验证
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

# 数据集-文献-基因表
class DatasetLiteratureGeneView(ModelViewSet):
    serializer_class = DatasetLiteratureGeneSerializer
    # 分页
    pagination_class = CustomeDatabalesPagination
    renderer_classes = [DatatablesRenderer]
    filter_backends = [DatatablesFilterBackend]
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['gene_name'] = self.request.query_params.get('gene_name')
        context['cell_type'] = self.request.query_params.get('cell_type')
        return context
    
    def get_queryset(self):
        pmid = self.request.query_params.get('pmid', None)
        gene_name = self.request.query_params.get('gene_name', None)
        cell_type = self.request.query_params.get('cell_type', None)
        species_name = self.request.query_params.get('species_name', None)
        queryset = dataset_info.objects.all().order_by('dataset_id')
        if pmid is not None:
            queryset = queryset.filter(literature__pmid=pmid)
        if gene_name is not None:
            queryset = queryset.filter(gene_expression__gene_name=gene_name)
        if cell_type is not None:
            queryset = queryset.filter(gene_expression__cell_types__icontains=cell_type)
        if species_name is not None:
            queryset = queryset.filter(species_name=species_name)
        return queryset
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # 列表和详情视图允许任何人访问
            permission_classes = [AllowAny]
        else:
            # 其他视图需要身份验证
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
# 提交-文献-数据集
class DatasetAndLiteratureCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        dataset_serializer = DatasetInfoSerializer(data=request.data)
        literature_serializer = LiteratureInfoSerializer(data=request.data)
        valid_dataset = dataset_serializer.is_valid()
        if dataset_serializer.is_valid() and literature_serializer.is_valid():
            dataset = dataset_serializer.save()
            literature = literature_serializer.save()

            # 建立关联关系
            dataset.literature.add(literature)

            return Response({"message": "Data submitted successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response(f"error {valid_dataset}",status=status.HTTP_400_BAD_REQUEST)
  
# 提交-矩阵文件     
class UploadedMatrixFileView(ModelViewSet):
    permission_classes = [IsAuthenticated]  # 限制只有登录用户能够访问
    serializer_class = UploadedMatrixFileSerializer

    def get_queryset(self):
        user = self.request.user
        return matrix_file.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
# 测试
def test(request):
    pmid = request.GET.get("pmid")
    literature = get_object_or_404(literature_dataset, pmid=pmid)
    dataset_ids = literature.dataset_info.values_list('dataset_id', flat=True)
    return HttpResponse(dataset_ids)
