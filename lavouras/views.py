from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from .models import Lote, Talhao
from .serializers import LoteSerializer, TalhaoSerializer


class TalhaoViewSet(viewsets.ModelViewSet):
    queryset = Talhao.objects.all()
    serializer_class = TalhaoSerializer

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError:
            raise ValidationError("Exclua os lotes vinculados antes de excluir o talhão.")


class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
