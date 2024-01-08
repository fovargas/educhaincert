from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('microcredenciales/', views.lista_microcredenciales, name='lista_microcredenciales'),
    path('admin/microcredenciales/', views.admin_microcredenciales, name='admin_microcredenciales'),
    path('admin/microcredenciales/emitir/<int:microcredencial_id>/', views.emitir_microcredencial, name='emitir_microcredencial'),
]