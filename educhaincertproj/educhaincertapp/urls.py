from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('microcredenciales/', views.lista_microcredenciales, name='lista_microcredenciales'),
    path('admin/microcredenciales/', views.admin_microcredenciales, name='admin_microcredenciales'),
    path('admin/microcredenciales/descargar_archivo/<int:id_microcredencial>/', views.descargar_archivo, name='descargar_archivo'),
]