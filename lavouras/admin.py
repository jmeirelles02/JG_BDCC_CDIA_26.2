from django.contrib import admin
from .models import Lote, Talhao

admin.site.register([Talhao, Lote])
admin.site.site_header = "Lavoura Inteligente"
admin.site.site_title = "Lavoura Inteligente"
