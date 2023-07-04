from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="celldb-home"),
    path("download", views.download, name="celldb-download"),
    path("upload", views.upload, name="celldb-upload"),
    path("overview", views.overview, name="celldb-overview"),
    path("plot", views.plotScatter, name="celldb-plot"),
    path("test", views.test, name="celldb-test"),
]
