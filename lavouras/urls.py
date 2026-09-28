from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import LoteViewSet, TalhaoViewSet

router = DefaultRouter()
router.register("talhoes", TalhaoViewSet)
router.register("lotes", LoteViewSet)
urlpatterns = [path("", include(router.urls))]
