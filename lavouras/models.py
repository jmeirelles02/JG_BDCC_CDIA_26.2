from django.db import models


class Talhao(models.Model):
    codigo = models.CharField(max_length=40, unique=True)
    nome = models.CharField(max_length=120)
    cultura = models.CharField(max_length=80)
    produtor = models.CharField(max_length=160)
    geometria = models.JSONField(help_text="Geometria GeoJSON do talhão.")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["codigo"]
        verbose_name = "talhão"
        verbose_name_plural = "talhões"

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Lote(models.Model):
    class Status(models.TextChoices):
        APROVADO = "APROVADO", "Aprovado"
        REVISAO = "REVISAO", "Revisão"
        BLOQUEADO = "BLOQUEADO", "Bloqueado"

    codigo = models.CharField(max_length=40, unique=True)
    talhao = models.ForeignKey(Talhao, on_delete=models.PROTECT, related_name="lotes")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.REVISAO)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "lote"
        verbose_name_plural = "lotes"

    def __str__(self):
        return f"{self.codigo} - {self.status}"
