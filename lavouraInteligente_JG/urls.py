from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def healthcheck(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("", healthcheck),
    path("admin/", admin.site.urls),
    path("api/", include("lavouras.urls")),
]
