from django.contrib import admin
from .models import Universidad, Estudiante, Microcredencial, Transaccion

admin.site.register(Universidad)
admin.site.register(Estudiante)
admin.site.register(Microcredencial)
admin.site.register(Transaccion)