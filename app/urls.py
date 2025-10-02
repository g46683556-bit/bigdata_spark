from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("generar/", views.generar_lote, name="generar"),
    path("upload_csv/", views.upload_csv, name="upload_csv"),
    path("graficos/", views.graficos, name="graficos"),  # 👈 nueva página
]
