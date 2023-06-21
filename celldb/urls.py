from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="celldb-home"),
    path("data", views.data, name="celldb-data"),
    path("search", views.search, name="celldb-search"),
    path("plot", views.plotScatter, name="celldb-plot"),
    path("test", views.test, name="celldb-test"),
]