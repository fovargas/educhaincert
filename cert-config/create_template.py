#!/usr/bin/env python

import json
import os

import configargparse

from cert_tools import helpers
from cert_tools import jsonpath_helpers

from cert_schema import BLOCKCERTS_V3_CONTEXT, VERIFIABLE_CREDENTIAL_V1_CONTEXT

def create_credential_subject_section():
    return {
        'id': "*|PUBKEY|*",
    }

def create_credential_display_section():
    return {
        "contentMediaType": "text/html",
        "content": "*|HTML_CONTENT|*"
    }

def create_v3_assertion(config):
    assertion = {
        '@context': [
            VERIFIABLE_CREDENTIAL_V1_CONTEXT,
            BLOCKCERTS_V3_CONTEXT,
            'https://raw.githubusercontent.com/fovargas/blockutpl/main/issuer-config/context.json'
        ],
        'type': ["VerifiableCredential", "BlockcertsCredential", "MCCUCredential"],
        "issuer": config.issuer_id,
        'issuanceDate': '*|DATE|*',
        'id': helpers.URN_UUID_PREFIX + '*|CERTUID|*'
    }
    return assertion


def create_v3_template(config):
    assertion = create_v3_assertion(config)
    credential_subject = create_credential_subject_section()

    assertion['credentialSubject'] = credential_subject

    if config.display_html:
        credential_display = create_credential_display_section()
        assertion['display'] = credential_display
        
    if config.additional_global_fields:
        for field in config.additional_global_fields:
            assertion = jsonpath_helpers.set_field(assertion, field['path'], field['value'])

    if config.additional_per_recipient_fields:
        for field in config.additional_per_recipient_fields:
            assertion = jsonpath_helpers.set_field(assertion, field['path'], field['value'])

    return assertion

def write_certificate_template(config):
    template_dir = config.template_dir
    if not os.path.isabs(template_dir):
        template_dir = os.path.join(config.abs_data_dir, template_dir)
    template_file_name = config.template_file_name

    assertion = create_v3_template(config)
    template_path = os.path.join(config.abs_data_dir, template_dir, template_file_name)

    print('Writing template to ' + template_path)
    with open(template_path, 'w') as cert_template:
        json.dump(assertion, cert_template)

def get_config():
    cwd = os.getcwd()
    config_file_path = os.path.join(cwd, 'conf.ini')
    p = configargparse.getArgumentParser(default_config_files=[config_file_path])

    p.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')

    p.add_argument('--data_dir', type=str, help='where data files are located')
    p.add_argument('--issuer_url', type=str, help='issuer URL')
    p.add_argument('--issuer_id', required=True, type=str, help='issuer profile')
    p.add_argument('--template_dir', type=str, help='the template output directory')
    p.add_argument('--display_html', type=bool, help='if true, displayHtml will be added to the certificate')
    p.add_argument('--template_file_name', type=str, help='the template file name')
    p.add_argument('--additional_global_fields', action=helpers.make_action('global_fields'),
                   help='additional global fields')
    p.add_argument('--additional_per_recipient_fields', action=helpers.make_action('per_recipient_fields'),
                   help='additional per-recipient fields')

    args, _ = p.parse_known_args()
    args.abs_data_dir = os.path.abspath(os.path.join(cwd, args.data_dir))
    return args

def main():
    conf = get_config()
    write_certificate_template(conf)
    print('Created template!')

if __name__ == "__main__":
    main()