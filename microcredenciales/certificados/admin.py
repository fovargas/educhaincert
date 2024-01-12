import subprocess,os, shutil, re

from django.contrib import admin, messages
from django.conf import settings
from django.urls import reverse
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from .models import Universidad, UnidadOrganizativa, Curso, OfertaAcademica, Estudiante, Microcredencial, Instructor, NivelDeMaestria, RutaAprendizaje, ParticipacionCurso
from datetime import datetime

def generar_certificados_sin_firmar(request):
    valor = request.GET.get('oferta_academica__id__exact', '')

    if valor.isdigit():
        os.chdir(settings.CERT_CONFIG_DIR)
        config_tools_file = settings.CERT_CONFIG_DIR / 'conf-cert-tools.ini'
        comando = "python3 instantiate_certificate.py --my-config "+str(config_tools_file)+" --oferta_academica '"+valor+"'"
        subprocess.run(comando, shell=True, capture_output=True, text=True, cwd = os.getcwd())
    
    messages.success(request, f"Operaciones ejecutadas correctamente")

def buscar_microcredenciales_sin_firmar(oferta_academica_id):
    microcredenciales = Microcredencial.objects.filter(participacion_curso__oferta_academica_id=oferta_academica_id).filter(estado='SIN FIRMAR')
    return microcredenciales

def preprocesar_archivos(archivos_buscados, directorio_origen, directorio_destino):
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)

    for archivo in os.listdir(directorio_origen):
        for archivo_buscado in archivos_buscados:
            if archivo_buscado in archivo:
                ruta_completa_origen = os.path.join(directorio_origen, archivo)
                ruta_completa_destino = os.path.join(directorio_destino, archivo)
                shutil.copy2(ruta_completa_origen, ruta_completa_destino)
                break

def anadir_archivo_ipfs(nombre_archivo):
    try:
        os.chdir(settings.CERT_CONFIG_DIR/'data'/'blockchain_certificates')
        comando = "ipfs add "+nombre_archivo
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd = os.getcwd())
        ipfs_hash = re.search(r'added (\S+)', resultado.stdout)
        if ipfs_hash:
            return ipfs_hash.group(1)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando IPFS: {e}")
        return None
    
def actualizar_registro(microcredencial, ipfs_hash):
    fecha_hora_actual = datetime.now()
    microcredencial.fecha_firma = fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S")
    microcredencial.ipfs_hash = ipfs_hash
    microcredencial.estado = 'FIRMADA'
    microcredencial.save()

def procesar_archivos():
    os.chdir(settings.CERT_CONFIG_DIR/'custom_cert_issuer')
    conf_issuer_file = settings.CERT_CONFIG_DIR / 'conf-cert-issuer.ini'
    unsigned_certificates_dir = settings.CERT_CONFIG_DIR/'data'/'preprocessing_certificates'
    blockchain_certificates_dir = settings.CERT_CONFIG_DIR/'data'/'blockchain_certificates'
    key_file = settings.CERT_CONFIG_DIR / 'pk_issuer.txt'
    work_dir = settings.CERT_CONFIG_DIR / 'data'/'work'

    comando = "python3 main.py -c " + str(conf_issuer_file) + " --unsigned_certificates_dir=" + str(unsigned_certificates_dir) + " --blockchain_certificates_dir=" + str(blockchain_certificates_dir) + " --key_file=" + str(key_file) + " --work_dir=" + str(work_dir)
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd = os.getcwd())
    uuids = re.findall(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', resultado.stdout)

    for uuid in uuids:
        print(str(uuid)+".json")
        ipfs_hash = anadir_archivo_ipfs(str(uuid)+".json")
        microcredencial = Microcredencial.objects.get(uuid=uuid)
        actualizar_registro(microcredencial, ipfs_hash)

def vaciar_carpeta_temporal(ruta_directorio):
    if not os.path.isdir(ruta_directorio):
        print("La ruta proporcionada no es un directorio.")
        return
    
    for nombre in os.listdir(ruta_directorio):
        ruta_completa = os.path.join(ruta_directorio, nombre)

        if os.path.isfile(ruta_completa) or os.path.islink(ruta_completa):
            os.unlink(ruta_completa)
        elif os.path.isdir(ruta_completa):
            shutil.rmtree(ruta_completa)

    print("La carpeta ha sido vaciada.")

def firmar_certificados_pendientes(request):
    microcredenciales_uuid = []
    unsigned_certificates_dir = settings.CERT_CONFIG_DIR/'data'/'unsigned_certificates'
    preproccesing_certificates_dir = settings.CERT_CONFIG_DIR/'data'/'preprocessing_certificates'
    oferta_academica_id = request.GET.get('oferta_academica__id__exact', '')
    microcredenciales_sin_firmar = buscar_microcredenciales_sin_firmar(oferta_academica_id)

    if(microcredenciales_sin_firmar.count() == 0):
        messages.warning(request, f"No existen microcredenciales sin firmar para esta oferta académica")
        return

    for microcredencial in microcredenciales_sin_firmar:
        uuid = microcredencial.uuid
        microcredenciales_uuid.append(uuid+".json")

    preprocesar_archivos(microcredenciales_uuid, unsigned_certificates_dir, preproccesing_certificates_dir)
    procesar_archivos()
    vaciar_carpeta_temporal(preproccesing_certificates_dir)
    messages.success(request, f"Operaciones ejecutadas correctamente")

class OfertaAcademicaInline(admin.TabularInline):
    model = OfertaAcademica
    extra = 1

class UnidadOrganizativaInline(admin.TabularInline):
    model = UnidadOrganizativa
    extra = 1

class UniversidadAdmin(admin.ModelAdmin):
    
    def ver_unidades_organizativas(self, obj):
        count = obj.unidadorganizativa_set.count()
        url = reverse('admin:certificados_unidadorganizativa_changelist') + f'?universidad__id__exact={obj.id}'
        return format_html('<a href="{}">{} unidades Organizativas</a>', url, count)
    
    list_display = ['nombre', 'ver_unidades_organizativas']
    readonly_fields = ['did']
    
    ver_unidades_organizativas.short_description = 'Unidades Organizativas'

class OfertaAcademicaAdmin(admin.ModelAdmin):

    def mostrar_oferta(self, obj):
        return str(obj)
    
    def ver_participantes(self, obj):
        count = obj.participacioncurso_set.count()
        url = reverse('admin:certificados_participacioncurso_changelist') + f'?oferta_academica__id__exact={obj.id}'
        return format_html('<a href="{}">{} participantes</a>', url, count)
    
    list_display = ['mostrar_oferta', 'ver_participantes']
    
    mostrar_oferta.short_description = 'Oferta Académica'
    ver_participantes.short_description = 'Participantes'

class ParticipacionCursoAdmin(admin.ModelAdmin):

    def mostrar_participantes(self, obj):
        return str(obj)

    def ver_microcredenciales(self, obj):
        count = obj.microcredencial_set.count()
        url = reverse('admin:certificados_microcredencial_changelist') + f'?participacion_curso__id__exact={obj.id}'
        return format_html('<a href="{}">{} microcredenciales</a>', url, count)

    def changelist_view(self, request, extra_context=None):
        if 'action' in request.POST:
            if request.POST['action'] == 'generar_certificados_sin_firmar':
                if not request.POST.getlist(ACTION_CHECKBOX_NAME):
                    self.model.objects.all()
                    generar_certificados_sin_firmar(request)
                    return HttpResponseRedirect(request.get_full_path())
            elif request.POST['action'] == 'firmar_certificados_pendientes':
                if not request.POST.getlist(ACTION_CHECKBOX_NAME):
                    self.model.objects.all()
                    firmar_certificados_pendientes(request)
                    return HttpResponseRedirect(request.get_full_path())

        return super(ParticipacionCursoAdmin, self).changelist_view(request, extra_context)

    list_filter = ['oferta_academica']
    actions = [generar_certificados_sin_firmar, firmar_certificados_pendientes]
    list_display = ['mostrar_participantes', 'ver_microcredenciales', 'oferta_academica']

    mostrar_participantes.short_description = 'Participantes'
    ver_microcredenciales.short_description = 'Microcredenciales'

class UnidadOrganizativaAdmin(admin.ModelAdmin):
    readonly_fields = ['did']

class EstudianteAdmin(admin.ModelAdmin):
    readonly_fields = ['did']

class MicrocredencialAdmin(admin.ModelAdmin):
    def mostrar_microcredenciales(self, obj):
        return str(obj)

    def descargar_archivo(self, obj):
        if obj.ipfs_hash == None:
            return format_html('<p class="disabled">No disponible</p>')
        else:
            return format_html('<a href="{}" class="button">Descargar</a>', reverse('descargar_archivo', args=[obj.id]))

    list_display = [ 'mostrar_microcredenciales','descargar_archivo'] 
    readonly_fields = ['fecha_emision','fecha_firma','uuid','ipfs_hash','estado']

    mostrar_microcredenciales.short_description = 'Lista de microcredenciales'

    descargar_archivo.short_description = 'Descarga'
    descargar_archivo.allow_tags = True

class CursoAdmin(admin.ModelAdmin):

    def ver_ofertas_academicas(self, obj):
        count = obj.ofertaacademica_set.count()
        url = reverse('admin:certificados_ofertaacademica_changelist') + f'?curso__id__exact={obj.id}'
        return format_html('<a href="{}">{} ofertas académicas</a>', url, count)
    
    list_display = ['nombre', 'ver_ofertas_academicas']

    ver_ofertas_academicas.short_description = 'Ofertas académicas'

class InstructorAdmin(admin.ModelAdmin):
    readonly_fields = ['did']

generar_certificados_sin_firmar.short_description = 'Generar certificados sin firmar'
firmar_certificados_pendientes.short_description = 'Firmar certificados pendientes'

admin.site.register(Universidad, UniversidadAdmin)
admin.site.register(UnidadOrganizativa, UnidadOrganizativaAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(NivelDeMaestria)
admin.site.register(RutaAprendizaje)
admin.site.register(OfertaAcademica, OfertaAcademicaAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(ParticipacionCurso, ParticipacionCursoAdmin)
admin.site.register(Microcredencial, MicrocredencialAdmin)