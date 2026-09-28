from rest_framework import serializers
from .models import Lote, Talhao


class TalhaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talhao
        fields = ["id", "codigo", "nome", "cultura", "produtor", "geometria", "criado_em"]
        read_only_fields = ["id", "criado_em"]


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = ["id", "codigo", "talhao", "status", "criado_em"]
        read_only_fields = ["id", "criado_em"]
