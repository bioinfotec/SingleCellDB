from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf import settings


app_name = "api-v2"
urlpatterns = [
    # 测试
    path("test/", views.test),
    # 文献信息
    path("literarure/", views.LiteratureInfoView.as_view({"get": "list", "post": "create"})),
    re_path("literarure/(?P<pk>\w+)/$", views.LiteratureInfoView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
    # 数据集信息
    path("dataset/", views.DatasetInfoVeiw.as_view({"get": "list", "post": "create"})),
    re_path("dataset/(?P<pk>\w+)/$", views.DatasetInfoVeiw.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
    # 文献-数据集信息
    path("literature-dataset/", views.LiteratureDatasetVeiw.as_view({"get": "list"})),
    # 数据集-文献信息
    path("dataset-literature/", views.DatasetLiteratureVeiw.as_view({"get": "list"})),
    # 细胞信息
    path("cell/", views.CellInfoView.as_view({"get": "list", "post": "create"})),
    # 基因表达量
    path("gene-expression/", views.GeneExpressionView.as_view({"get": "list"})),
    # 基因信息
    path("gene-info/", views.GeneInfoView.as_view({"get": "list", "post": "create"})),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


urlpatterns = format_suffix_patterns(urlpatterns)
