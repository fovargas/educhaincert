# Proyecto: Modelo de gestión descentralizada para la emisión y verificación de microcredenciales

Este proyecto se enfoca en el desarrollo de un modelo de gestión descentralizada para la emisión y verificación de microcredenciales, utilizando tecnologías de cadena de bloques.

## Lenguaje de Programación

El proyecto está desarrollado en **Python**, un lenguaje de programación versátil y ampliamente utilizado.

## Librerías Utilizadas

Las siguientes librerías de Python se han utilizado en este proyecto:

- **Django**: Un framework de alto nivel para el desarrollo web.
- **Cert-tools**: Herramientas para crear plantillas de certificados y generar certificados sin firmar.
- **Cert-Issuer**: Para firmar certificados en la cadena de bloques.
- **Veramo**: Facilita la interacción con identidades y verificaciones descentralizadas.
- **IPFS (InterPlanetary File System)**: Un protocolo y red de pares para almacenar y compartir datos en un sistema de archivos distribuido.

## Comandos Utilizados

### Generar una Plantilla de Certificados

```bash
python3 create_template.py --my-config conf-cert-tools.ini
```

```bash
python3 create_template.py --my-config conf-cert-tools-eth.ini
```

### Crear Certificados sin Firmar a partir de una fuente de datos

```bash
python3 instantiate_certificate.py --my-config conf-cert-tools.ini
```

```bash
python3 instantiate_certificate.py --my-config conf-cert-tools-eth.ini
```

### Firmar Lotes de Certificados

Para certificados ubicados en projectpath/cert-config/data/unsigned_certificates

```bash
python3 custom_cert_issuer/main.py --my-config conf-cert-issuer.ini
```

```bash
python3 custom_cert_issuer/main.py --my-config conf-cert-issuer-eth.ini
```

