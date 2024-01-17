#!/usr/bin/env python

'''
Merges a certificate template with recipients defined in a roster file. The result is
unsigned certificates that can be given to cert-issuer.
'''
import copy
import csv
import json
import os
import uuid

from datetime import datetime, timezone

import mysql.connector
from mysql.connector import Error

import configargparse

from cert_schema import schema_validator

from cert_tools import helpers
from cert_tools import jsonpath_helpers

from cert_tools import instantiate_v3_certificate_batch as ic


class Recipient:
    def __init__(self, fields):

        self.pubkey = fields.pop('id_recipient')
        self.additional_fields = fields

def instantiate_display_content(cert, recipient):

    course_name = recipient.additional_fields['course']
    learning_path = recipient.additional_fields['learning_path']
    learning_outcome = recipient.additional_fields['learning_outcome']

    html_template = f"""<div><div style="background-color: #ffffff; padding: 20px;max-width: 500px;display: block;margin-left: auto;margin-right: auto;"><img style="max-width: 200px !important; display: block; margin-left: auto; margin-right: auto;" src="https://www.utpl.edu.ec/sites/default/files/archivos/marca%20UTPL%202018-03.png" /><div style="background-color: #f8f8f8; padding: 10px; color: #003f72;"><h2 style="text-align: center;">Microcredencial: {course_name}</h2></div><div style="background-color: #ffffff; padding: 20px; color: #003f72;text-align: justify;"><p><strong>&iexcl;Felicitaciones!</strong> Tu nueva microcredencial simboliza no solo tu compromiso y dedicaci&oacute;n, sino tambi&eacute;n la adquisici&oacute;n de las siguientes habilidades y competencias: <strong>{learning_outcome}.</strong></p><p>Esta microcredencial es un paso crucial en tu <em>Ruta de aprendizaje {learning_path}</em>, dise&ntilde;ada para ofrecerte una formaci&oacute;n integral y especializada. Est&aacute;s en el camino correcto para alcanzar tus metas profesionales y personales.</p><p>Tu viaje no termina aqu&iacute;. Cada paso que das ampl&iacute;a tus horizontes y te acerca a ser la versi&oacute;n m&aacute;s realizada de ti mismo. Contin&uacute;a avanzando, explorando y super&aacute;ndote.</p></div><div style="background-color: #f8f8f8; padding: 4px;"><h3 style="text-align: center; color: #004270;">#decideserm&aacute;s</h2></div></div></div>
    """.format(course_name=course_name, learning_path=learning_path, learning_outcome=learning_outcome)

    cert['display']['content'] = html_template
    return cert


def instantiate_recipient(cert, recipient, additional_fields):
    cert['credentialSubject']['id'] = recipient.pubkey

    if additional_fields:
        if not recipient.additional_fields:
            raise Exception('expected additional recipient fields but none found')
        for field in additional_fields:
            cert = jsonpath_helpers.set_field(cert, field['path'], recipient.additional_fields[field['csv_column']])
    else:
        if recipient.additional_fields:
            # throw an exception on this in case it's a user error. We may decide to remove this if it's a nuisance
            raise Exception(
                'there are fields that are not expected by the additional_per_recipient_fields configuration')

def create_iso8601_tz():
    return datetime.now(timezone.utc).isoformat()[:-13]+'Z'

def create_unsigned_certificates(template, recipients, use_identities, additionalFields, display_html):
    issued_on = create_iso8601_tz()

    cert_list = []
    for recipient in recipients:
        if use_identities:
            uid = recipient.identity
            uid = "".join(c for c in uid if c.isalnum())
        else:
            uid = str(uuid.uuid4())

        cert = copy.deepcopy(template)

        ic.instantiate_assertion(cert, uid, issued_on)
        if display_html:
            instantiate_display_content(cert, recipient)
        instantiate_recipient(cert, recipient, additionalFields)

        # validate unsigned certificate before writing
        schema_validator.validate_v3(cert, True)

        cert_list.append((cert, uid, recipient.additional_fields["id_participation"], issued_on))
    return cert_list

def get_recipients_from_roster(config):
    roster = os.path.join(config.abs_data_dir, config.roster)
    with open(roster, 'r') as theFile:
        reader = csv.DictReader(theFile)
        recipients = map(lambda x: Recipient(x), reader)
        return list(recipients)
    
def get_recipients_from_database(config, db_config):
    try:
        # Establece la conexión con la base de datos
        connection = mysql.connector.connect(
            host=db_config['db_host'],
            database=db_config['db_name'],
            user=db_config['db_user'],
            password=db_config['db_password']
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            # Ejecuta la consulta SQL
            query = """
                SELECT
                    p.id AS id_participation,
                    est.did AS id_recipient,
                    uni.did AS id_organization,
                    uo.did AS id_organizational_unit,
                    'Microcredential' AS type_credential,
                    inst.did AS id_instructor,
                    rap.nombre AS learning_path,
                    nm.nombre AS level_of_mastery,
                    cur.resultado_aprendizaje AS learning_outcome,
                    cur.nombre AS course
                FROM
                    educhaincertapp_participacioncurso p
                    JOIN educhaincertapp_estudiante est ON p.estudiante_id = est.id
                    JOIN educhaincertapp_ofertaacademica oa ON p.oferta_academica_id = oa.id
                    JOIN educhaincertapp_curso cur ON oa.curso_id = cur.id
                    JOIN educhaincertapp_instructor inst ON oa.instructor_id = inst.id
                    JOIN educhaincertapp_unidadorganizativa uo ON cur.unidad_organizativa_id = uo.id
                    JOIN educhaincertapp_rutaaprendizaje rap ON cur.ruta_aprendizaje_id = rap.id
                    JOIN educhaincertapp_universidad uni ON rap.universidad_id = uni.id
                    JOIN educhaincertapp_niveldemaestria nm ON cur.nivel_maestria_id = nm.id
                    LEFT JOIN educhaincertapp_microcredencial m ON p.id = m.participacion_curso_id
                WHERE m.participacion_curso_id IS NULL AND p.oferta_academica_id = %s AND p.estado = 'APROBADO';
            """
            cursor.execute(query, (config.oferta_academica_id,))
            # Procesa cada fila como un objeto Recipient
            recipients = [Recipient(row) for row in cursor]
            cursor.close()
            return recipients
    except Error as e:
        print("Error al conectarse a MySQL", e)
    finally:
        if connection.is_connected():
            connection.close()

def insertar_microcredencial(db_config, uuid, participation_id, issued_on):
    try:
        # Establecer conexión con la base de datos
        connection = mysql.connector.connect(
            host=db_config['db_host'],
            database=db_config['db_name'],
            user=db_config['db_user'],
            password=db_config['db_password']
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Consulta SQL para insertar un nuevo registro
            query = """
            INSERT INTO educhaincertapp_microcredencial (participacion_curso_id, estado, fecha_emision, uuid)
            VALUES (%s,'SIN FIRMAR',%s,%s)
            """
            cursor.execute(query, (participation_id, issued_on, uuid))

            # Confirmar la transacción
            connection.commit()

            print("Microcredencial insertada correctamente.")
    except Error as e:
        print("Error al insertar en MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Configuración de la base de datos
db_config = {
    'db_host': 'localhost',
    'db_name': 'educhaincert',
    'db_user': 'utpl',
    'db_password': 'utpl'
}

def instantiate_batch(config):
    recipients = get_recipients_from_database(config, db_config)
    template = ic.get_template(config)
    use_identities = config.filename_format == "certname_identity"
    cert_list = create_unsigned_certificates(template, recipients, use_identities, config.additional_per_recipient_fields, config.display_html)
    output_dir = os.path.join(config.abs_data_dir, config.unsigned_certificates_dir)
    print('Writing certificates to ' + output_dir)

    for cert in cert_list:
        cert_file = os.path.join(output_dir, cert[1] + '.json')
        if os.path.isfile(cert_file) and config.no_clobber:
            continue

        with open(cert_file, 'w') as unsigned_cert:
            json.dump(cert[0], unsigned_cert)
        
        insertar_microcredencial(db_config, cert[1], cert[2], datetime.fromisoformat(cert[3].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S'))


def get_config():
    cwd = os.getcwd()

    p = configargparse.getArgumentParser(default_config_files=[os.path.join(cwd, 'conf.ini')])
    p.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    p.add_argument('--data_dir', type=str, help='where data files are located')
    p.add_argument('--template_dir', type=str, help='the template output directory')
    p.add_argument('--template_file_name', type=str, help='the template file name')
    p.add_argument('--display_html', type=bool, help='if true, displayHtml will be added to the certificate')
    p.add_argument('--additional_per_recipient_fields', action=helpers.make_action('per_recipient_fields'), help='additional per-recipient fields')
    p.add_argument('--unsigned_certificates_dir', type=str, help='output directory for unsigned certificates')
    p.add_argument('--roster', type=str, help='roster file name')
    p.add_argument('--filename_format', type=str, help='how to format certificate filenames (one of certname_identity or uuid)')
    p.add_argument('--no_clobber', action='store_true', help='whether to overwrite existing certificates')
    p.add_argument('--oferta_academica_id', type=str, help='oferta academica')
    args, _ = p.parse_known_args()
    args.abs_data_dir = os.path.abspath(os.path.join(cwd, args.data_dir))

    return args


def main():
    conf = get_config()
    instantiate_batch(conf)
    print('Instantiated batch!')

if __name__ == "__main__":
    main()