from celldb_v2.models import literature_info, literature_dataset, dataset_info
from .serializers import literature_info_serializer,literature_dataset_serializer, dataset_info_serializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# 文献信息
class LiteratureInfoView(ModelViewSet):
    queryset = literature_info.objects.all()
    serializer_class = literature_info_serializer
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
    queryset = literature_dataset.objects.all()
    serializer_class = literature_dataset_serializer
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # 列表和详情视图允许任何人访问
            permission_classes = [AllowAny]
        else:
            # 其他视图需要身份验证
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
def test(request):
    dataset = literature_dataset.objects.all()[1]
    return HttpResponse(dataset)
