from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("tran/", views.getTran, name="api-tran"),
    path("tran/<int:id>", views.getTran_detail),
    path('my-view/', views.MyView.as_view(), name='my-view'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
