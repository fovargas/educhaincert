import subprocess,os
from django.db import models

class Universidad(models.Model):
    nombre = models.CharField(max_length=255)
    did = models.CharField(max_length=255, blank=True, null=True, editable=False)
    logo = models.ImageField(upload_to='logos_universidades/')

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        os.chdir('../veramo')
        comando = "npx veramo did generate -i 'did:key' -k 'local' -a '"+self.nombre+"'"

        # Si la universidad es nueva y no tiene DID
        if not self.did:
            # Ejecutar el comando para generar DID
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd = os.getcwd())
            # Capturar la salida del comando y almacenarla en el campo DID
            self.did = resultado.stdout.strip()
        super().save(*args, **kwargs)

class UnidadOrganizativa(models.Model):
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    did = models.CharField(max_length=255, blank=True, null=True, editable=False)

    def __str__(self):
        return self.universidad.nombre+" - "+self.nombre
    
    def save(self, *args, **kwargs):

        universidad = Universidad.objects.get(id=self.universidad.pk)  # Obtiene un libro específico
        universidad_nombre = universidad.nombre

        os.chdir('../veramo')
        comando = "npx veramo did generate -i 'did:key' -k 'local' -a '"+universidad_nombre+" - "+self.nombre+"'"

        # Si la unidad organizativa es nueva y no tiene DID
        if not self.did:
            # Ejecutar el comando para generar DID
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd = os.getcwd())
            # Capturar la salida del comando y almacenarla en el campo DID
            self.did = resultado.stdout.strip()
        super().save(*args, **kwargs)

class NivelDeMaestria(models.Model):
    nombre = models.CharField(max_length=255)

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

        # Si la universidad es nueva y no tiene DID
        if not self.did:
            # Ejecutar el comando para generar DID
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd = os.getcwd())
            # Capturar la salida del comando y almacenarla en el campo DID
            self.did = resultado.stdout.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Instructor(models.Model):
    identificacion = models.CharField(max_length=255, unique=True)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    did = models.CharField(max_length=255, blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        os.chdir('../veramo')
        comando = "npx veramo did generate -i 'did:key' -k 'local' -a '"+self.identificacion+"'"

        # Si la universidad es nueva y no tiene DID
        if not self.did:
            # Ejecutar el comando para generar DID
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd = os.getcwd())
            # Capturar la salida del comando y almacenarla en el campo DID
            self.did = resultado.stdout.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
class RutaAprendizaje(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(max_length=1024)
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE)

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

    def __str__(self):
        return self.estudiante.nombre+" - "+self.oferta_academica.curso.nombre+" - "+self.oferta_academica.periodo

class Microcredencial(models.Model):
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    inscripcion = models.ForeignKey(ParticipacionCurso, on_delete=models.CASCADE)
    fecha_emision = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.estudiante.nombre+" - "+self.oferta_academica.curso.nombre+" - "+self.oferta_academica.periodo
