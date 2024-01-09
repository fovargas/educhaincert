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

import configargparse

from cert_schema import schema_validator

from cert_tools import helpers
from cert_tools import jsonpath_helpers

from cert_tools import instantiate_v3_certificate_batch as ic


class Recipient:
    def __init__(self, fields):
        # Mostly keeping it for compatibility with existing rosters but if it's a problem,
        # we can remove it and individual's can add them in via 'additional_per_recipient_fields'
        self.pubkey = fields.pop('pubkey')

        self.additional_fields = fields

def instantiate_display_content(cert, recipient):

    course_name = recipient.additional_fields['course']
    learning_path = recipient.additional_fields['learning_path']
    learning_outcome = recipient.additional_fields['learning_outcome']

    html_template = f"""<section><div style="background-color: #ffffff; padding: 20px;max-width: 500px;display: block;margin-left: auto;margin-right: auto;"><img style="max-width: 200px !important; display: block; margin-left: auto; margin-right: auto;" src="https://www.utpl.edu.ec/sites/default/files/archivos/marca%20UTPL%202018-03.png" /><div style="background-color: #f8f8f8; padding: 10px; color: #003f72;"><h2 style="text-align: center;">Microcredencial: {course_name}</h2></div><div style="background-color: #ffffff; padding: 20px; color: #003f72;text-align: justify;"><p><strong>&iexcl;Felicitaciones!</strong> Tu nueva microcredencial simboliza no solo tu compromiso y dedicaci&oacute;n, sino tambi&eacute;n la adquisici&oacute;n de las siguientes habilidades y competencias: <strong>{learning_outcome}.</strong></p><p>Esta microcredencial es un paso crucial en tu <em>Ruta de aprendizaje {learning_path}</em>, dise&ntilde;ada para ofrecerte una formaci&oacute;n integral y especializada. Est&aacute;s en el camino correcto para alcanzar tus metas profesionales y personales.</p><p>Tu viaje no termina aqu&iacute;. Cada paso que das ampl&iacute;a tus horizontes y te acerca a ser la versi&oacute;n m&aacute;s realizada de ti mismo. Contin&uacute;a avanzando, explorando y super&aacute;ndote.</p></div><div style="background-color: #f8f8f8; padding: 4px;"><h3 style="text-align: center; color: #004270;">#decideserm&aacute;s</h2></div></div></section>
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


def create_unsigned_certificates_from_roster(template, recipients, use_identities, additionalFields, display_html):
    issued_on = helpers.create_iso8601_tz()

    certs = {}
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

        certs[uid] = cert
    return certs

def get_recipients_from_roster(config):
    roster = os.path.join(config.abs_data_dir, config.roster)
    with open(roster, 'r') as theFile:
        reader = csv.DictReader(theFile)
        recipients = map(lambda x: Recipient(x), reader)
        return list(recipients)

def instantiate_batch(config):
    recipients = get_recipients_from_roster(config)
    template = ic.get_template(config)
    use_identities = config.filename_format == "certname_identity"
    certs = create_unsigned_certificates_from_roster(template, recipients, use_identities, config.additional_per_recipient_fields, config.display_html)
    output_dir = os.path.join(config.abs_data_dir, config.unsigned_certificates_dir)
    print('Writing certificates to ' + output_dir)

    for uid in certs.keys():
        cert_file = os.path.join(output_dir, uid + '.json')
        if os.path.isfile(cert_file) and config.no_clobber:
            continue

        with open(cert_file, 'w') as unsigned_cert:
            json.dump(certs[uid], unsigned_cert)


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
    args, _ = p.parse_known_args()
    args.abs_data_dir = os.path.abspath(os.path.join(cwd, args.data_dir))

    return args


def main():
    conf = get_config()
    instantiate_batch(conf)
    print('Instantiated batch!')


if __name__ == "__main__":
    main()