from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf import settings


app_name = "api-v2"
urlpatterns = [
    # 测试
    path("test/", views.test),
    #文献信息
    path("literarure/", views.LiteratureInfoView.as_view({"get": "list", "post": "create"})),
    re_path("literarure/(?P<pk>\w+)/$", views.LiteratureInfoView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
    #数据集信息
    path("dataset/", views.DatasetInfoVeiw.as_view({"get": "list", "post": "create"})),
    re_path("dataset/(?P<pk>\w+)/$", views.DatasetInfoVeiw.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


urlpatterns = format_suffix_patterns(urlpatterns)
