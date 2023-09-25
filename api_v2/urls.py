from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf import settings


app_name = "api-v2"
urlpatterns = [
    # 删除
    path("literature-delete/<str:pmid>/", views.literature_delete),
    # 测试
    path("test/<str:pk>/", views.LiteratureMixinView.as_view()),
    path("test/", views.LiteratureMixinView.as_view()),
    # 文献信息
    path("literature/", views.LiteratureInfoView.as_view({"get": "list", "post": "create"})),
    re_path("literature/(?P<pk>\w+)/$", views.LiteratureInfoView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
    # 数据集信息
    path("dataset/", views.DatasetInfoVeiw.as_view({"get": "list", "post": "create"})),
    re_path("dataset/(?P<pk>\w+)/$", views.DatasetInfoVeiw.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
    # 文献-数据集信息
    path("literature-dataset/", views.LiteratureDatasetVeiw.as_view({"get": "list"})),
    # 数据集-文献信息
    path("dataset-literature/", views.DatasetLiteratureVeiw.as_view({"get": "list"})),
    # 细胞信息
    path("cell-info/", views.CellInfoView.as_view({"get": "list", "post": "create"})),
    # 基因表达量
    path("gene-expression/", views.GeneExpressionView.as_view({"get": "list"})),
    # 基因信息
    path("gene-info/", views.GeneInfoView.as_view({"get": "list", "post": "create"})),
    # 细胞类型信息
    path("cell-type-info/", views.CellTypeView.as_view({"get": "list", "post": "create"})),
    # 数据集-文献-基因信息
    path("dataset-literature-gene/", views.DatasetLiteratureGeneView.as_view({"get": "list"})),
    # 提交-文献-数据
    path("upload-literature-dataset/", views.DatasetAndLiteratureCreateView.as_view()),
    # 提交-矩阵文件
    path("upload-matrix-file/", views.UploadedMatrixFileView.as_view({"post": "create", "get": "list"})),
    # 查询-矩阵文件
    path("list-matrix-file/", views.ListMatrixFileListView.as_view()),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


urlpatterns = format_suffix_patterns(urlpatterns)
