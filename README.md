# Proyecto: Modelo de gestión descentralizada para la emisión y verificación de microcredenciales

Este proyecto se enfoca en el desarrollo de un modelo de gestión descentralizada para la emisión y verificación de microcredenciales, utilizando tecnologías de cadena de bloques.

## Lenguaje de Programación

El proyecto está desarrollado en **Python**, un lenguaje de programación versátil y ampliamente utilizado.

## Librerías Utilizadas

Las siguientes librerías de Python se han utilizado en este proyecto:

- **Django**: Un framework de alto nivel para el desarrollo web.
- **Cert-tools**: Herramientas para crear plantillas de certificados.
- **Cert-Issuer**: Para emitir certificados en la blockchain.
- **Veramo**: Facilita la interacción con identidades y verificaciones descentralizadas.
- **IPFS (InterPlanetary File System)**: Un protocolo y red de pares para almacenar y compartir datos en un sistema de archivos distribuido.

## Comandos Utilizados

### Generar una Plantilla de Certificados

```bash
create-certificate-template --my-config conf-cert-tools.ini
```

### Crear Certificados sin Firmar a partir de un archivo roster (CSV):

```bash
instantiate-certificate-batch -c conf-cert-tools.ini
```

### Firmar Lotes de Certificados

Para certificados ubicados en projectpath/cert-config/data/unsigned_certificates

```bash
cert-issuer -c conf-cert-issuer.ini
```