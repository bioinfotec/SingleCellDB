from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="celldb-home"),
    # path("search/", views.search, name="celldb-browse"),
    path("browse-feature/", views.browseFeature, name="celldb-browse-feature"),
    path("browse-expression/", views.browseExpression, name="celldb-browse-expression"),
    path("download", views.download, name="celldb-download"),
    path("upload", views.upload, name="celldb-upload"),
    path("overview", views.overview, name="celldb-overview"),
    path("plot/", views.plotScatter, name="celldb-plot"),
    path("plot/local", views.plotLocal, name="celldb-plot-local"),
    path("plot/r", views.plotR, name="celldb-plot-r"),
    path("runcode/", views.runCode, name="celldb-runcode"),
    path("analyse/", views.analyse, name="celldb-analyse"),
    path("test", views.test, name="celldb-test"),
    path("test2", views.test2, name="celldb-test2"),
]
