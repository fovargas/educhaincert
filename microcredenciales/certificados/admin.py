from django.contrib import admin
from .models import Universidad, UnidadOrganizativa, Curso, OfertaAcademica, Estudiante, Microcredencial, Instructor, NivelDeMaestria, RutaAprendizaje, ParticipacionCurso

admin.site.register(Curso)
admin.site.register(OfertaAcademica)
admin.site.register(NivelDeMaestria)
admin.site.register(RutaAprendizaje)
admin.site.register(Microcredencial)
admin.site.register(ParticipacionCurso)

class UniversidadAdmin(admin.ModelAdmin):
    readonly_fields = ['did']

class UnidadOrganizativaAdmin(admin.ModelAdmin):
    readonly_fields = ['did']

class EstudianteAdmin(admin.ModelAdmin):
    readonly_fields = ['did']

class InstructorAdmin(admin.ModelAdmin):
    readonly_fields = ['did']

admin.site.register(Universidad, UniversidadAdmin)
admin.site.register(UnidadOrganizativa, UnidadOrganizativaAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Instructor, InstructorAdmin)