import subprocess,os
from django.db import models

class Universidad(models.Model):
    nombre = models.CharField(max_length=255)
    did = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='logos_universidades/')

    

    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        os.chdir('../veramo')
        comando = "npx veramo did generate -i 'did:key' -k 'local' -a 'nasa'"

        # Si la universidad es nueva y no tiene DID
        if not self.did:
            # Ejecutar el comando para generar DID
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, cwd = os.getcwd())
            # Capturar la salida del comando y almacenarla en el campo DID
            self.did = resultado.stdout.strip()
        super().save(*args, **kwargs)

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
