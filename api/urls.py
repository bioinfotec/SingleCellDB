from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

#For photo File
from django.conf.urls.static import static
from django.conf import settings
app_name = "api"
urlpatterns = [
    path("tran/", views.getTran, name="api-tran"),
    path("tran/<int:id>", views.getTran_detail),
    path("tran/all", views.getTran_all, name="api-tran-all"),
    path(
        "dataset/", 
        views.DataSetView.as_view({"get": "list", "post": "create"}),
        name="api-geo",
    ),
    re_path("dataset/(?P<pk>\w+)/$", views.DataSetView.as_view({"get": "retrieve"})),
    
    #For File download
    path("download", views.download_file, name="api-download"),
    
    #For photo file
    path("savefile", views.SaveFiles, name="api-savefile")
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


urlpatterns = format_suffix_patterns(urlpatterns)
