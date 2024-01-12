import subprocess,os
from django.db import models

class Universidad(models.Model):
    nombre = models.CharField(max_length=255)
    did = models.CharField(max_length=255, blank=True, null=True, editable=False)
    logo = models.ImageField(upload_to='logos_universidades/')

    class Meta:
        verbose_name_plural = "universidades"
    
    def save(self, *args, **kwargs):
        os.chdir('../veramo')
        comando = "npx veramo did generate -i 'did:key' -k 'local' -a '"+self.nombre+"'"

        if not self.did:
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd = os.getcwd())
            self.did = resultado.stdout.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
class UnidadOrganizativa(models.Model):
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    did = models.CharField(max_length=255, blank=True, null=True, editable=False)

    class Meta:
        verbose_name_plural = "unidades organizativas"
    
    def save(self, *args, **kwargs):

        universidad = Universidad.objects.get(id=self.universidad.pk)
        universidad_nombre = universidad.nombre

        os.chdir('../veramo')
        comando = "npx veramo did generate -i 'did:key' -k 'local' -a '"+universidad_nombre+" - "+self.nombre+"'"

        if not self.did:
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd = os.getcwd())
            self.did = resultado.stdout.strip()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.universidad.nombre+" - "+self.nombre

class NivelDeMaestria(models.Model):
    nombre = models.CharField(max_length=255)

    class Meta:
        verbose_name = "nivel de maestría"
        verbose_name_plural = "niveles de maestría"

    def __str__(self):
        return self.nombre

class Estudiante(models.Model):
    identificacion = models.CharField(max_length=255, unique=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    did = models.CharField(max_length=255, blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        os.chdir('../veramo')
        comando = "npx veramo did generate -i 'did:key' -k 'local' -a '"+self.identificacion+"'"

        if not self.did:
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd = os.getcwd())
            self.did = resultado.stdout.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Instructor(models.Model):
    identificacion = models.CharField(max_length=255, unique=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    did = models.CharField(max_length=255, blank=True, null=True, editable=False)

    class Meta:
        verbose_name_plural = "instructores"
    
    def save(self, *args, **kwargs):
        os.chdir('../veramo')
        comando = "npx veramo did generate -i 'did:key' -k 'local' -a '"+self.identificacion+"'"

        if not self.did:
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd = os.getcwd())
            self.did = resultado.stdout.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
    
    
class RutaAprendizaje(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(max_length=1024)
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "ruta de aprendizaje"
        verbose_name_plural = "rutas de aprendizaje"

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    unidad_organizativa = models.ForeignKey(UnidadOrganizativa, on_delete=models.CASCADE)
    nivel_maestria = models.ForeignKey(NivelDeMaestria, on_delete=models.CASCADE)
    resultado_aprendizaje = models.TextField(max_length=1024)
    ruta_aprendizaje = models.ForeignKey(RutaAprendizaje, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class OfertaAcademica(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    periodo = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "oferta académica"
        verbose_name_plural = "ofertas académicas"
    
    def __str__(self):
        return self.curso.nombre+" - "+self.periodo
    
class ParticipacionCurso(models.Model):

    estados = (
        ('aprobado', 'APROBADO'),
        ('reprobado', 'REPROBADO'),
        ('validado', 'VALIDADO'),
    )

    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    oferta_academica = models.ForeignKey(OfertaAcademica, on_delete=models.CASCADE)
    calificacion = models.FloatField(blank=True, null=True)
    estado = models.CharField(max_length=255, blank=True, null=True, choices=estados)

    class Meta:
        verbose_name = "participante"
        verbose_name_plural = "participantes"
    
    def __str__(self):
        return self.estudiante.nombre+" - "+self.oferta_academica.curso.nombre+" - "+self.oferta_academica.periodo

class Microcredencial(models.Model):
    participacion_curso = models.ForeignKey(ParticipacionCurso, on_delete=models.CASCADE)
    fecha_emision = models.DateTimeField(blank=True, null=True)
    fecha_firma = models.DateTimeField(blank=True, null=True)
    uuid = models.CharField(max_length=255, blank=True, null=True)
    ipfs_hash = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "microcredenciales"
    
    def __str__(self):
        return self.participacion_curso.estudiante.nombre+" - "+self.participacion_curso.oferta_academica.curso.nombre+" - "+self.participacion_curso.oferta_academica.periodo