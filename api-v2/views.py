from celldb_v2.models import literature_info, literature_dataset, dataset_info,cell_info, gene_expression,gene_info, cell_type_info
from .serializers import LiteratureInfoSerializer, DatasetInfoSerializer, DatasetLiteratureSerializer, LiteratureDatasetSerializer, CellInfoSerializer,GeneExpressionSerializer, GeneInfoSerializer, CellTypeInfoSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q, F

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

        return queryset.filter(filters)
    
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

# 测试
def test(request):
    pmid = request.GET.get("pmid")
    literature = get_object_or_404(literature_dataset, pmid=pmid)
    dataset_ids = literature.dataset_info.values_list('dataset_id', flat=True)
    return HttpResponse(dataset_ids)
