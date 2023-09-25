from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("celldb.urls")),
    path("api/", include("api.urls")),
    path("api-v2/", include("api_v2.urls")),
    path("api-rpy2/", include("api_rpy2.urls")),
    path("task/", include("task1.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
