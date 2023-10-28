from django.db import models

class Universidad(models.Model):
    nombre = models.CharField(max_length=255)
    # Otros campos relevantes

class Estudiante(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # Otros campos relevantes

class Microcredencial(models.Model):
    universidad = models.ForeignKey(Universidad, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    contenido_IPFS = models.CharField(max_length=255)  # CID de IPFS

class Transaccion(models.Model):
    microcredencial = models.ForeignKey(Microcredencial, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
